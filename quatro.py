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

    def intersects(self, ax, ay, bx, by, sizex, sizey):

        if ax < 0:
            return True
        if ay < 0:
            return True
        if bx >= sizex:
            return True
        if by >= sizey:
            return True

        # they are "side by side" :)
        if self.bx < ax:
            return False
        if bx < self.ax:
            return False
        if self.by < ay:
            return False
        if by < self.ay:
            return False

        # it is entirely inside:
        if ax > self.ax and self.bx > bx and ay > self.ay and self.by > by:
            return False
        # it is entirely inside:
        if ax < self.ax and self.bx < bx and ay < self.ay and self.by < by:
            return False

        return True


class squares:
    def __init__(self, sizex, sizey):
        self.squares = []
        self.sizex = sizex
        self.sizey = sizey

    def add_square(self, sq):
        self.squares += [sq]

    def intersecting(self, ax, ay, bx, by, not_this_one=None):

        for sq in self.squares:
            if sq == not_this_one:
                continue
            if sq.intersects(ax, ay, bx, by, self.sizex, self.sizey):
               return True
        return False


    def add_non_intersecting_square(self):
        ok = False
        for _ in range(1000):
            ax = randrange(0, self.sizex)
            ay = randrange(0, self.sizey)
            size = randrange(8, 300)
            bx = ax + size
            by = ay + size
            if bx >= self.sizex:
                continue
            if by >= self.sizey:
                continue
            # verify existing squares conflicts
            if self.intersecting(ax, ay, bx, by):
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
        for sq in self.squares:
            can_move = True
            if self.intersecting(sq.ax+sq.dx, sq.ay+sq.dy, sq.bx+sq.dx, sq.by+sq.dy, not_this_one=sq):
                sq.dx *= -1
                sq.dy *= -1
            else:
                sq.ax += sq.dx
                sq.ay += sq.dy
                sq.bx += sq.dx
                sq.by += sq.dy

    def generate_image(self):
        size = self.sizex, self.sizey
        im = Image.new('RGBA', size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        for sq in self.squares:
            draw.rectangle((sq.ax, sq.ay, sq.bx, sq.by), fill=None, width=1)

        return im

    def generate_video(self):
        pass


def main():
    sqs = squares(640, 480)
    for _ in range(200):
        sqs.add_non_intersecting_square()
    print(sqs)

    for i in range(4000):
        im = sqs.generate_image()
        im.save(f'squares{i:04}.png', 'PNG')
        sqs.do_move()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
