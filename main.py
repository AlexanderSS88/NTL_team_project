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

                if input("Should program use json file? ('j' to use json):\t") == 'j':
                    print(bot.bot_cycle(work_w_json=True))
                else:
                    print(bot.bot_cycle())
