from testutil import testinit
from testspaceinvaders import testspaceinvaders
from testasteroids import testasteroids
from testpacman import testpacman


def main():
    testinit(44100, 2)
    testasteroids()
    testspaceinvaders()
    testpacman()


if __name__ == "__main__":
    main()