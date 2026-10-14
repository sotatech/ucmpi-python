from comfort import ComfortConnection


def main():
    comfort = ComfortConnection()

    comfort.connect()
    comfort.read_loop()


if __name__ == "__main__":
    main()
    