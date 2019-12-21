from PIL import Image, ImageDraw

class Captcha(object):
    def __init__(self,path):
        self.img = Image.open(path)
        self.imgs = []
        self.t2val = {}

    def getImgs(self,len,size):
        self.convert()
        self.twoValue(198)
        self.clearNoise(N=3,Z=1)
        self.saveImg()
        self.sliceImg(len)
        self.resizeImgs(size)
        
        return self.imgs

    def convert(self):
        self.img = self.img.convert('L')

    def twoValue(self,G):
        self.t2val = {}
        for y in range(0, self.img.size[1]):
            for x in range(0, self.img.size[0]):
                g = self.img.getpixel((x, y))
                if g > G:
                    self.t2val[(x, y)] = 1
                else:
                    self.t2val[(x, y)] = 0
    
    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败
    def clearNoise(self, N, Z):
        for i in range(0, Z):
            self.t2val[(0, 0)] = 1
            self.t2val[(self.img.size[0] - 1, self.img.size[1] - 1)] = 1

            for x in range(1, self.img.size[0] - 1):
                for y in range(1, self.img.size[1] - 1):
                    nearDots = 0
                    L = self.t2val[(x, y)]
                    ddx = [-1,0,1]
                    ddy = [-1,0,1]
                    for dx in ddx:
                        for dy in ddy:
                            if dx == 0 and dy == 0:
                                continue
                            if L == self.t2val[(x+dx,y+dy)]:
                                nearDots += 1
                    if nearDots < N:
                        self.t2val[(x, y)] = 1

    def saveImg(self):
        image = Image.new("1",self.img.size)
        draw  = ImageDraw.Draw(image)
        for x in range(0, self.img.size[0]):
            for y in range(0, self.img.size[1]):
                draw.point((x, y), self.t2val[(x, y)])
        self.img = image

    def sliceImg(self,count=4, p_w=3):

        '''
        :param count: 
        :param p_w: 对切割地方多少像素内进行判断
        '''
        w, h = self.img.size
        pixdata = self.img.load()
        eachWidth = int(w / count)
        beforeX = 0
        self.imgs = []
        for i in range(count):

            allBCount = []
            nextXOri = (i + 1) * eachWidth
            for x in range(nextXOri - p_w, nextXOri + p_w):
                if x >= w:
                    x = w - 1
                if x < 0:
                    x = 0
                b_count = 0
                for y in range(h):
                    if pixdata[x, y] == 0:
                        b_count += 1
                allBCount.append({'x_pos': x, 'count': b_count})

            sort = sorted(allBCount, key=lambda e: e.get('count'))
            nextX = sort[0]['x_pos']
            box = (beforeX, 0, nextX, h)
            beforeX = nextX
            self.imgs.append(self.img.crop(box))

    def resizeImgs(self,size):
        for i in range(len(self.imgs)):
            self.imgs[i] = self.imgs[i].resize(size)
           
