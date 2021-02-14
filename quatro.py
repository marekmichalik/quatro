import os
from random import randrange, choice
from PIL import Image, ImageDraw

FRAMES = 1000  # number of frames of viedo
SQUARES = 100  # squares count
SIZE_X = 1920  # video dimensions in pixels
SIZE_Y = 1080
TEMP_FILE = 'quatro.gif'
OUTPUT_FILE = 'quatro.webm'


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

    def intersects(self, ax, ay, bx, by):
        if ax < 0:
            return True
        if ay < 0:
            return True
        if bx >= SIZE_X:
            return True
        if by >= SIZE_Y:
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

    def intersects_vertically(self, ax, ay, bx, by):  # dx should change
        if ax < 0:
            return True
        if bx >= SIZE_X:
            return True

        # they are "side by side" :)
        if self.bx < ax:
            return False
        if bx < self.ax:
            return False

        if (ax == self.ax or ax == self.bx or bx == self.ax or bx == self.bx) and (self.ay <= ay <= self.by or self.ay <= by <= self.by or ay <= self.ay <= by or ay <= self.by <= by):
            return True

        return False

    def intersects_horizontally(self, ax, ay, bx, by):  # dy should change
        if ay < 0:
            return True
        if by >= SIZE_Y:
            return True

        # they are "side by side" :)
        if self.by < ay:
            return False
        if by < self.ay:
            return False

        if (ay == self.ay or ay == self.by or by == self.ay or by == self.by ) and (self.ax <= ax <= self.bx or self.ax <= bx <= self.bx or ax <= self.ax <= bx or ax <= self.bx <= bx):
            return True

        return False


class squares:
    def __init__(self):
        self.squares = []

    def add_square(self, sq):
        self.squares += [sq]

    def intersecting(self, ax, ay, bx, by, not_this_one=None):

        for sq in self.squares:
            if sq == not_this_one:
                continue
            if sq.intersects(ax, ay, bx, by):
               return True
        return False

    def intersecting_vertically(self, ax, ay, bx, by, not_this_one=None):

        for sq in self.squares:
            if sq == not_this_one:
                continue
            if sq.intersects_vertically(ax, ay, bx, by):
               return True
        return False

    def intersecting_horizontally(self, ax, ay, bx, by, not_this_one=None):

        for sq in self.squares:
            if sq == not_this_one:
                continue
            if sq.intersects_horizontally(ax, ay, bx, by):
               return True
        return False

    def add_non_intersecting_square(self):
        ok = False
        for _ in range(1000):
            ax = randrange(0, SIZE_X)
            ay = randrange(0, SIZE_Y)
            size = randrange(8, 300)
            bx = ax + size
            by = ay + size
            if bx >= SIZE_X:
                continue
            if by >= SIZE_Y:
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

            # bounce

            if self.intersecting_vertically(sq.ax+sq.dx, sq.ay+sq.dy, sq.bx+sq.dx, sq.by+sq.dy, not_this_one=sq):
                sq.dx *= -1
                can_move = False

            # bounce
            if self.intersecting_horizontally(sq.ax+sq.dx, sq.ay+sq.dy, sq.bx+sq.dx, sq.by+sq.dy, not_this_one=sq):
                sq.dy *= -1
                can_move = False

            # just move
            if can_move:
                sq.ax += sq.dx
                sq.ay += sq.dy
                sq.bx += sq.dx
                sq.by += sq.dy

    def generate_image(self):
        size = SIZE_X, SIZE_Y
        im = Image.new('RGB', size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        for sq in self.squares:
            draw.rectangle((sq.ax, sq.ay, sq.bx, sq.by), fill=None, width=1)

        return im

    def generate_new_image(self):
        print('.', end='', flush=True)
        self.do_move()
        return self.generate_image()

    def generate_video(self):
        im = self.generate_image()
        # save as .gif
        im.save(TEMP_FILE,
                save_all=True,
                append_images=[self.generate_new_image() for _ in range(FRAMES-1)],
                duration=16.666,
                loop=0,
                minimize_size=True)

        # Convert to video (.webm)
        import moviepy.editor as mp
        clip = mp.VideoFileClip(TEMP_FILE)
        clip.write_videofile(OUTPUT_FILE, audio=False, threads=1, preset='fast',
                             ffmpeg_params=['-vf', 'fps=60', '-ss', '5', '-crf', '30', '-b:v', '0'])
        clip.close()

        os.remove(TEMP_FILE)


def main():
    # generate squares
    sqs = squares()
    for _ in range(SQUARES):
        sqs.add_non_intersecting_square()
    print(sqs)

    sqs.generate_video()


if __name__ == "__main__":
    main()
