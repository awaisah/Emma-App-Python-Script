import os, io, json, random

# Load the file names from the avatars directory
directory = os.fsencode("avatars")
files = os.listdir(directory)

occupations = []
lorem = ""
contacts = []

# Load a list of occupations for randomly selection for each contact
# and lorem ipsum file for generating profile
with open('occupations.json') as fOccupations, open('loremipsum.txt') as fLorem:
  occupations = json.load(fOccupations)
  lorem = fLorem.readlines()[0].split(". ")
  
  fOccupations.close()
  fLorem.close()


# List of all items in the directory ending with ".png"
files = filter(lambda filename: filename.decode('ascii').endswith(".png"), files)

# This will contain the text which will be used to output into requires.txt
requiresForJS = '{\n'

# Loop through every third element in the sorted list of images
for filename in sorted(files)[::3]:
    filename = filename.decode('ascii')

    if filename:
        # Create a dictionary for contact's details
        name = filename.split(".")[0]

        # Javascript had an issue working with whitespace (' ') in require() so this is used to remove it
        safeName = name.replace(" ", "_")

        requiresForJS += '"'+name+'": require("./'+safeName+'.png"),\n'

        # Replace File Names for js
        os.rename("avatars/"+name+".png","avatars/"+safeName+".png")
        os.rename("avatars/"+name+"@2x.png","avatars/"+safeName+"@2x.png")
        os.rename("avatars/"+name+"@3x.png","avatars/"+safeName+"@3x.png")

        profile = ""
        # Select 5 random sentances from the lorem string to make profile
        for i in range(0,5):
            profile += lorem[random.randint(0,len(lorem)-1)]+". "

        # Add to the contacts array. This will be the output for contacts.json
        contacts.append({
            "name": name,
            "imageName": safeName+".png",
            "occupation": occupations[random.randint(0, len(occupations)-1)],
            "profile": profile
        })

requiresForJS += "}"


# Export the file 
with io.open('contacts.json', 'w', encoding='utf-8') as f, io.open('requires.txt', 'w', encoding='utf-8') as fRequires:
  f.write(json.dumps(contacts, indent=4))
  fRequires.write(requiresForJS)
  print("SUCCESS: Exported contacts.json with contacts details. Exported requires.txt with code to enter into the index.js file in the React Native project (assets/avatars/index.js file)")
  f.close()
  fRequires.close()