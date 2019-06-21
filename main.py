import PIL.Image
import PIL.ImageDraw


def main():
    data_size = (64, 64)
    im = PIL.Image.new('RGB', data_size, color='red')
    d = PIL.ImageDraw.Draw(im)
    d.text((10, 10), 'Hello, world')

    im = im.resize([s * 10 for s in data_size])
    im.save('data/output/sample.png')


if __name__ == '__main__':
    main()
