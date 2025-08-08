import time
import os

# ANSI color codes
YELLOW = '\033[93m'
GOLD = '\033[33m'
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
BLINK = '\033[5m'
RESET = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_viral_buddha():
    clear_screen()
    
    print(f"{BOLD}{YELLOW}╔══════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{YELLOW}║                    🔥 VIRAL BUDDHA CODE 🔥                    ║{RESET}")
    print(f"{BOLD}{YELLOW}╚══════════════════════════════════════════════════════════════╝{RESET}")
    print()
    
    buddha_lines = [
        f"{GOLD}                       _oo0oo_{RESET}",
        f"{GOLD}                      o8888888o{RESET}",
        f"{GOLD}                      88\" . \"88{RESET}",
        f"{GOLD}                      (| {RED}-_-{GOLD} |){RESET}",
        f"{GOLD}                      0\\  {RED}={GOLD}  /0{RESET}",
        f"{GOLD}                    ___/`---'\\___{RESET}",
        f"{GOLD}                  .' \\\\|     |// '.{RESET}",
        f"{GOLD}                 / \\\\|||  :  |||// \\{RESET}",
        f"{GOLD}                / _||||| {RED}-:-{GOLD} |||||_ \\{RESET}",
        f"{GOLD}               |   | \\\\\\  {RED}-{GOLD}  /// |   |{RESET}",
        f"{GOLD}               | \\_|  ''\\{RED}---{GOLD}/''  |_/ |{RESET}",
        f"{GOLD}               \\  .-\\__  '{RED}-{GOLD}'  ___/-. /{RESET}",
        f"{GOLD}             ___'. .'  /{RED}--{GOLD}.{RED}--{GOLD}\\  `. .'___{RESET}",
        f"{GOLD}          .\"\" '<  `.___\\_{RED}<|>{GOLD}_/___.' >' \"\".{RESET}",
        f"{GOLD}         | | :  `- \\`.;`\\ {RED}_{GOLD} /`;.`/ - ` : | |{RESET}",
        f"{GOLD}         \\  \\ `_.   \\_ __{RED}\\{GOLD} /{RED}__{GOLD} _/   .-` /  /{RESET}",
        f"{GOLD}     =====`-.____`.___ \\{RED}_____{GOLD}/___.-`___.-'====={RESET}",
        f"{GOLD}                       `={RED}---{GOLD}='{RESET}",
    ]
    
    for line in buddha_lines:
        print(line)
        time.sleep(0.1)
    
    print()
    print(f"{BOLD}{BLINK}{CYAN}★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★{RESET}")
    print(f"{BOLD}{GREEN}              🙏 PHẬT PHÙ HỘ - KHÔNG BAO GIỜ BUG! 🙏{RESET}")
    print(f"{BOLD}{PURPLE}                  💻 CODE LIKE A BUDDHA 💻{RESET}")
    print(f"{BOLD}{BLUE}                    ✨ NO BUGS, NO CRY ✨{RESET}")
    print(f"{BOLD}{BLINK}{CYAN}★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★{RESET}")
    print()
    
    motivational_quotes = [
        f"{BOLD}{WHITE}💡 'Debug với tâm hồn thanh tịnh, bug sẽ tự biến mất!' 💡{RESET}",
        f"{BOLD}{WHITE}🧘 'Kiên nhẫn là chìa khóa của mọi thuật toán!' 🧘{RESET}",
        f"{BOLD}{WHITE}⚡ 'Code sạch, tâm trong, bug không còn!' ⚡{RESET}",
        f"{BOLD}{WHITE}🌟 'Buddha bless this code!' 🌟{RESET}"
    ]
    
    for quote in motivational_quotes:
        print(quote)
        time.sleep(0.8)
    
    print()
    print(f"{BOLD}{YELLOW}🔥 SHARE THIS VIRAL BUDDHA TO YOUR CODING FRIENDS! 🔥{RESET}")
    print(f"{BOLD}{RED}❤️  Like & Subscribe for more CODING BLESSINGS! ❤️{RESET}")

# Run the viral Buddha only if this file is executed directly
if __name__ == "__main__":
    print_viral_buddha()