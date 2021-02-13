from random import randrange, choice
from PIL import Image, ImageDraw

class square:
    def __init__(self, ax, ay, bx, by, dx, dy):
        # square defined by two points: (ax, ay) and (bx, by)
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f'a[{self.ax}, {self.ay}], b[{self.bx}, {self.by}]: [{self.dx}, {self.dy}]'


class squares:
    def __init__(self, sizex, sizey):
        self.squares = []
        self.sizex = sizex
        self.sizey = sizey

    def add_square(self, sq):
        self.squares += [sq]

    def add_non_conflicting_square(self):
        for _ in range(100):
            ax = randrange(0, self.sizex)
            ay = randrange(0, self.sizey)
            size = randrange(100)
            bx = ax + size
            by = ay + size
            if bx >= self.sizex:
                continue
            if by >= self.sizey:
                continue
            # todo: verify existing squares conflicts


        dx = choice([-1, 1])
        dy = choice([-1, 1])
        sq = square(ax, ay, bx, by, dx, dy)
        self.add_square(sq)

    def __str__(self):
        result = ''
        for each in self.squares:
            result += each.__str__() + '\n'
        return result

    def do_move(self):
        pass

    def generate_image(self):
        size = self.sizex, self.sizey
        im = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        for sq in self.squares:
            draw.rectangle((sq.ax, sq.ay, sq.bx, sq.by), fill=128)

        return im

    def generate_video(self):
        pass



def main():
    sqs = squares(640, 480)
    for _ in range(5):
        sqs.add_non_conflicting_square()

    print(sqs)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
