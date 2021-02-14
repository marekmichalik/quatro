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

    def conflict(self, ax, ay, bx, by):
        # it is entirely inside:
        if ax < self.ax < self.bx < bx and ay < self.ay < self.by < by:
            return False

        # they are "side by side" :)
        if self.bx < ax:
            return False
        if bx < self.ax:
            return False
        if self.by < ay:
            return False
        if by < self.ay:
            return False



        return True
class squares:
    def __init__(self, sizex, sizey):
        self.squares = []
        self.sizex = sizex
        self.sizey = sizey

    def add_square(self, sq):
        self.squares += [sq]

    def add_non_conflicting_square(self):
        ok = False
        for _ in range(1000):
            ax = randrange(0, self.sizex)
            ay = randrange(0, self.sizey)
            size = randrange(30, 200)
            bx = ax + size
            by = ay + size
            if bx >= self.sizex:
                continue
            if by >= self.sizey:
                continue
            # verify existing squares conflicts
            conflict = False
            for sq in self.squares:
                if sq.conflict(ax, ay, bx, by):
                    conflict = True
                    break
            if conflict:
                continue

            ok = True
            break

        if not ok:
            return

        dx = choice([-1, 1])
        dy = choice([-1, 1])
        sq = square(ax, ay, bx, by, dx, dy)
        self.add_square(sq)

    def __str__(self):
        result = ''
        for each in self.squares:
            result += each.__str__() + '\n'
        result += str(len(self.squares))
        return result

    def do_move(self):
        pass

    def generate_image(self):
        size = self.sizex, self.sizey
        im = Image.new('RGBA', size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        for sq in self.squares:
            draw.rectangle((sq.ax, sq.ay, sq.bx, sq.by), fill=None, width=1)
            im.save('try.png', 'PNG')
        return im

    def generate_video(self):
        pass


def main():
    sqs = squares(640, 480)
    for _ in range(20):
        sqs.add_non_conflicting_square()

    sqs.generate_image()
    print(sqs)




if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
