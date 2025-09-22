print("What is your sign?")
sign = input()
if sign == "Aries":
    print("  /\\      /\\")
    print(" /  \\    /  \\")
    print("     \\  /")
    print("      \\/")
if sign == "Taurus":
    print(" .     .")
    print(" '.___.'")
    print(" .'   '.")
    print(":       :")
    print(":       :")
    print(" '.___.'")
if sign == "Gemini":
    print("._____.")
    print("  | |")
    print("  | |")
    print(" _|_|_")
    print("'     '")
if sign == "Cancer":
    print("   .--.")
    print("  /   _'.")
    print(" (_) ( )")
    print("'.    /")
    print("  '--'")
if sign == "Leo":
    print("  .--.")
    print(" (    )")
    print("(_ )  /")
    print("    (_.")
if sign == "Virgo":
    print(" _")
    print("' ':--.--.")
    print("   |  |  |_")
    print("   |  |  | )")
    print("   |  |  |/")
    print("        (J")
if sign == "Libra":
    print("     __")
    print("___.'  '.___")
    print("____________")
if sign == "Scorpio":
    print(" _")
    print("' ':--.--.")
    print("   |  |  |")
    print("   |  |  |  ...")
    print("         '---':")
if sign == "Sagittarius":
    print("      ...")
    print("      .':")
    print("    .'")
    print("'..'")
    print(".''.")
if sign == "Capricorn":
    print("        _")
    print("\\      /_)")
    print(" \\    /'.")
    print("  \\  /   :")
    print("   \\/ __.'")
if sign == "Aquarius":
    print(".-\"-._.-\"-._.-")
    print(".-\"-._.-\"-._.-")
if sign == "Pisces":
    print("'- .    .-'")
    print(" --:--:--")
    print("   :  :")
    print(".-'    '-.")
if sign != "Aries" and sign != "Taurus" and sign != "Gemini" and sign != "Cancer" and sign != "Leo" and sign != "Virgo" and sign != "Libra" and sign != "Scorpio" and sign != "Sagittarius" and sign != "Capricorn" and sign != "Aquarius" and sign != "Pisces":
    print("Unknown sign")  # This will be printed if the input does not match any zodiac sign.