from flask import Flask, Response, send_file, render_template, request, redirect
from PIL import Image
from datetime import datetime
import os 
CURRENT_DIRECTORY = os.getcwd()
app = Flask(__name__)
def resize_image(img, width=None, height=None):
    if width and height:
        img_resize = img.resize((width, height))
    else:
        original_width, original_height = img.size    
        img_resize = img.resize(__resize_factory(original_width, original_height, width,height))
    return img_resize

def __resize_factory(original_width, original_height,width,height):    
    if width:
        percent_change = (width*100)/original_width
        new_height = int(original_height*(percent_change/100))
        return (width, new_height)
    elif height:
        percent_change = (height*100)/original_height
        new_width = int(original_width*(percent_change/100))
        return (new_width, height)

def trans_paste(fg_img, bg_img, alpha=1.0, box=(0,0)):
    fg_img_trans = Image.new("RGBA",fg_img.size)
    fg_img_trans = Image.blend(fg_img_trans,fg_img,alpha)
    bg_img.paste(fg_img_trans,box,fg_img_trans)
    return bg_img

@app.route("/")
def index():
    return render_template('docs/index.html')

@app.route("/upload-image/", methods=['GET', 'POST'])
def upload_image():
    context = dict()
    if (request.method=='POST'):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        context['msg'] = "imagem Enviada!"
        file = request.files['image']
        names = file.filename.split('.')
        file.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens',  '{}.{}'.format(int(timestamp), names[1])))
    return render_template('docs/upload-image.html', **context)

@app.route("/upload-logo/", methods=['GET', 'POST'])
def upload_logo():
    context = dict()
    if (request.method=='POST'):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        context['msg'] = "imagem Enviada!"
        context['class'] = "success"
        file = request.files['image']
        names = file.filename.split('.')
        if names[1] in ['png', 'PNG']:
            file.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas',  '{}.{}'.format(int(timestamp), names[1])))
        else:
            context['msg'] = "A imagem deve permitir transparecencia [PNG]"
            context['class'] = "danger"

    return render_template('docs/upload-logo.html', **context)

@app.route("/get-images/")
def get_form_images():
    images = os.listdir(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens'))
    marcas = os.listdir(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas'))

    return render_template('docs/get-images.html', imagens=images, magua=marcas)

@app.route("/image/", methods=['GET', ])
def image():
    image = request.args.get('image')
    width = request.args.get('width', default=0, type=int)
    height = request.args.get('height', default=0, type=int)
    marca = request.args.get('marca')
    filename = image.split('.')

    if width or height:
        new_name = __new_image_name_factory(filename[0],filename[1],width,height)
    else:
        new_name = image

    # if not os.path.isfile(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name)):
    #     img = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image))
    #     img_resize = resize_image(img, width=width, height=height)
    #     img_resize.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), optimized=True) 
    
    # if marca:
    #     new_image = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name))
    #     marca_image = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'marcas', marca))
    #     width_of_marca = int(new_image.width*(25/100))
    #     marca_new_image = resize_image(marca_image, width=width_of_marca)
    #     new_image = trans_paste(marca_new_image, new_image, 0.5, (100,100))
    #     new_image = new_image.convert("RGB")
    #     new_image.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), optimized=True) 
    
    crop_on_heights(new_name, [337,500,900], 145)
    # new_name = 'tt{}'.format(new_name)
    # return send_file(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', new_name), mimetype='image/jpeg')

def __new_image_name_factory(name,file_extension,width,height):
    if width and height:
        new_name = "{}_{}_{}.{}".format(name,height,width,file_extension)
    elif width:
        new_name = "{}_w{}.{}".format(name,width,file_extension)
    elif height:
        new_name = "{}_h{}.{}".format(name,height,file_extension)
    return new_name
    

def crop_on_heights(image_name, heights, maximum_crop_height):
    index = 0
    
    image = Image.open(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image_name)).convert('RGB')
    
    original_width, original_height = image.size
    
    where_height_is_cropping = 0

    heights.append(original_height)

    final_height = False

    cutting_heights = []

    #@TODO: FINISH THIS BAD BOY
    # while(not final_height):
    for height in heights:
        
        # if(heights)
        where_height_is_cropping += maximum_crop_height
        if(where_height_is_cropping >= height):
            cutting_heights.append(height)
            continue

        while(where_height_is_cropping < height):

            cutting_heights.append(where_height_is_cropping)
            where_height_is_cropping+=maximum_crop_height
        
        # if
        where_height_is_cropping = height
                

    print(sum(cutting_heights))
    print(cutting_heights)
    for height in cutting_heights:
        
        im = image.crop((0, where_height_is_cropping, original_width, height))
        where_height_is_cropping = height
        image_name = 'index_{}.jpg'.format(index)
        index += 1
        im.save(os.path.join(CURRENT_DIRECTORY, 'uploads', 'imagens', image_name ), "JPEG", optimized=True)

if __name__ == '__main__':
    app.run(debug=True)