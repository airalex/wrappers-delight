import PIL.Image
import PIL.ImageDraw


def main():
    im = PIL.Image.new('RGB', (64, 64), color='red')
    d = PIL.ImageDraw.Draw(im)
    d.text((10, 10), 'Hello, world')

    im.save('data/output/sample.png')


if __name__ == '__main__':
    main()
