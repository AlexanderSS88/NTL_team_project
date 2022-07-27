from vk_tools.cls_application import Application

if __name__ == '__main__':

    while True:
        command = input("Please choose the command: \n"
                        "'b' -start bot, \n"
                        "'q'- to quit: \t")
        match command:
            case 'q':
                break
            case 'b':
                bot = Application()
                print(bot.bot_cycle())

