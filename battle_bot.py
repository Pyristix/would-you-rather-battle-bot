import os
import random
import discord
import pandas as pd
import sklearn as skl
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

random.seed()
client = discord.Client()

enemies = ["bears", "bees", "horses", "ducks", "dogs", "cats", "fire ants", "eagles", "bats", "sharks", "dolphins", "cavemen", "soldiers", "wrestlers", "doctors", "lawyers", "T-Rexes", "vampires", "werewolves", "wizards"]
current_battle = None;


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global current_battle
    if message.author == client.user:   #Makes sure that the bot doesn't respond to its own messages
        return
        
    if message.content == '$bb$start':
        if current_battle == None:
            current_battle = await create_selection(message)
            await predict_choice(message, current_battle)
        else:
            await message.channel.send('Would you rather battle ' + str(current_battle[0]) + " " + enemies[current_battle[1]] + ' or ' + str(current_battle[2]) + " " + enemies[current_battle[3]] + '?')
            await predict_choice(message, current_battle)
            
    if message.content.startswith('$bb$select'):
        if current_battle == None:
            await message.channel.send('Please start a battle before selecting')
        else:
            await append_result(message, message.content[11:])
            
    if message.content == '$bb$reset':
        reset_data(message.author.name)
        await message.channel.send('Your battle data has been reset')

#Creates a random battle
async def create_selection(message):
    enemy_1_amount = random.randint(2,100)
    enemy_1_type = random.randint(0,19)
    enemy_2_amount = random.randint(2,100)
    enemy_2_type = random.randint(0,19)
    await message.channel.send('Would you rather battle ' + str(enemy_1_amount) + " " + enemies[enemy_1_type] + ' or ' + str(enemy_2_amount) + " " + enemies[enemy_2_type] + '?')
    return [enemy_1_amount, enemy_1_type, enemy_2_amount, enemy_2_type]
    
#Uses neural network to predict what the user will choose based on his past decisions
async def predict_choice(message, current_battle):
    data_files = os.listdir("./")
    data_files.remove(__file__)
    
    for file in data_files:
        if not (file[-9:] == "_data.csv"):
            data_files.remove(file)
    
    dataframe = pd.DataFrame()

    #Adds the user's battle data to the dataframe
    if message.author.name + "_data.csv" in data_files:
        try:
            dataframe = pd.read_csv(message.author.name + "_data.csv", header = None)
        except pd.errors.EmptyDataError:
            print("Notice: User data file is empty")
    
    #Adds all other user data to the dataframe if the user doesn't have any data or has not enough data
    if dataframe.size < 50:
        if message.author.name + "_data.csv" in data_files:
            data_files.remove(message.author.name + "_data.csv")
        for file_name in data_files:
            try:
                temp_dataframe = pd.read_csv(file_name, header = None)
                dataframe = dataframe.append(temp_dataframe, ignore_index = True)
            except pd.errors.EmptyDataError:
                print("Notice: " + file_name + " is empty")
    
    if dataframe.size < 50:
        await message.channel.send("There is not enough data to predict your decision")
        return
        
    features = [0,1,2,3]
    x = dataframe[features]
    y = dataframe[4]
    
    current_battle_data = pd.DataFrame([[current_battle[0], current_battle[1], current_battle[2], current_battle[3]]])
    
    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)
    
    neural_network = MLPClassifier(hidden_layer_sizes=(4,4,4))
    neural_network.fit(x, y)
    
    await message.channel.send("It is predicted that you will choose option " + str(neural_network.predict(current_battle_data)))

#Records outcome of battle for future reference by the neural network
async def append_result(message, choice):
    global current_battle
    decision_integer = 0
    
    if choice == str(current_battle[0]) + " " + str(enemies[current_battle[1]]):
        decision_integer = 1
    elif choice == str(current_battle[2]) + " " + str(enemies[current_battle[3]]):
        decision_integer = 2
    else:
        await message.channel.send('Please choose one of the options')
        return
        
    user_datafile = open(message.author.name + "_data.csv", "a")
    user_datafile.write(str(current_battle[0]) + "," + str(current_battle[1]) + "," + str(current_battle[2]) + "," + str(current_battle[3]) + "," + str(decision_integer) + "\n")
    
    await message.channel.send('Battle completed')
    current_battle = None
    
#Clears previous battle data for a specific user
def reset_data(username):
    try:
        os.remove(username + "_data.csv")
    except:
        print(username + " attempted to reset but their data file is empty")
    
    
    
client.run("############") #Insert Discord bot token inside the quotation marks
