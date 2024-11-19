import json

#stores presets and remaining filament
filament_presets = {}

#load saved filament data
def load_data():
    try:
        with open('filament_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#saves data to json file
def save_data():
    with open('filament_data.json', 'w') as file:
        json.dump(filament_presets, file, indent=4)

#displays presets as numbered list
def display_numbered_presets():
    if not filament_presets:
        print("No presets available. Add one using the option '2. Add new filament preset'")
    else:
        print("Available Filament Presets:")
        for i, (key, value) in enumerate(filament_presets.items(), 1):
            print(f"{i}. {key} - {value['remaining']}g remaining")
    print()

#adds a new preset to numbered list, initializes with 1000g
def add_preset():
    brand = input("Enter the filament brand (e.g., Bambu, Push_Plastic): ")
    filament_type = input("Enter filament type (e.g., PLA_Matte, PETG): ")
    filament_color = input("Enter filament color (e.g., Red, Blue): ")
    preset_name = f"{brand} - {filament_type} - {filament_color}"

    #creates new preset with 1000g if not duplicate
    if preset_name not in filament_presets:
        filament_presets[preset_name] = {"remaining": 1000.0}

    print(f"Preset '{preset_name}' added!")
    save_data()

#used filament and subtracts total from amount remaining in preset
def use_filament():
    display_numbered_presets()
    if not filament_presets:
        return  #edge case: no presets

    try:
        preset_number = int(input("Enter the number of the filament preset you are using: "))
        preset_name = list(filament_presets.keys())[preset_number - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return
    
    used_amount = float(input("Enter the amount of filament used in grams: "))
    if used_amount < 0:
        print("Amount used must be a positive number.")
        return

    if filament_presets[preset_name]["remaining"] - used_amount < 0:
        print(f"Warning: You don't have enough filament. You only have {filament_presets[preset_name]['remaining']}g remaining.")
    else:
        filament_presets[preset_name]["remaining"] -= used_amount
        print(f"{used_amount}g used. {filament_presets[preset_name]['remaining']}g remaining for {preset_name}.")

    save_data()

#resets preset to 1000g when using a new spool of an already existing preset
def reset_spool():
    display_numbered_presets()
    if not filament_presets:
        return  # No presets to reset

    try:
        preset_number = int(input("Enter the number of the filament preset you are resetting: "))
        preset_name = list(filament_presets.keys())[preset_number - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return
    
    filament_presets[preset_name]["remaining"] = 1000.0
    print(f"Filament preset '{preset_name}' has been reset to 1000g.")
    save_data()

#deletes outdated/unused preset
def delete_preset():
    display_numbered_presets()
    if not filament_presets:
        return  #edge case: preset list is empty

    try:
        preset_number = int(input("Enter the number of the filament preset you want to delete: "))
        preset_name = list(filament_presets.keys())[preset_number - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return

    #deletion confirmation
    confirm = input(f"Are you sure you want to delete the preset '{preset_name}'? (y/n): ").strip().lower()
    if confirm == 'y':
        del filament_presets[preset_name]
        print(f"Preset '{preset_name}' has been deleted.")
        save_data()
    else:
        print("Preset deletion canceled.")

def main():
    global filament_presets
    filament_presets = load_data()

    while True:
        print("1. Show available presets")
        print("2. Add new filament preset")
        print("3. Use filament")
        print("4. Reset spool (new spool)")
        print("5. Delete a preset")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_numbered_presets()
        elif choice == '2':
            add_preset()
        elif choice == '3':
            use_filament()
        elif choice == '4':
            reset_spool()
        elif choice == '5':
            delete_preset()
        elif choice == '6':
            print("Exiting program...")
            break
        else:
            print("Invalid option. Please try again.")
        print()

if __name__ == "__main__":
    main()
