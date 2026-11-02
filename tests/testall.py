from testutil import testinit
from testexample import testexample
from testspaceinvaders import testspaceinvaders
from testasteroids import testasteroids
from testpacman import testpacman


def main():
    testinit(44100, 2)
    testexample()
    testasteroids()
    testspaceinvaders()
    testpacman()


if __name__ == "__main__":
    main()