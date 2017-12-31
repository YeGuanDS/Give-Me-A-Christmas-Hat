import sys
import cv2
import dlib

# add a hat for person in the photo
def add_hat(img,hat_img):
    # preprocess hat image
    r,g,b,a = cv2.split(hat_img) #channels
    rgb_hat = cv2.merge((r,g,b))

    cv2.imwrite("hat_alpha.jpg",a)

    ## face detection with dlib

    # dlib face landmark detection
    predictor_path = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)  

    # dlib frontal face detection
    detector = dlib.get_frontal_face_detector()
    dets = detector(img, 1)

    # if found
    if len(dets)>0:  
        for d in dets:
            x,y,w,h = d.left(),d.top(), d.right()-d.left(), d.bottom()-d.top()
            shape = predictor(img, d)

            # edge points of eyes
            point1 = shape.part(0)
            point2 = shape.part(2)

            # get center
            eyes_center = ((point1.x+point2.x)//2,(point1.y+point2.y)//2)

            #  adaptive hat size
            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w/rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w/rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1
            resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))

            # use alpha channel as mask
            mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
            mask_inv =  cv2.bitwise_not(mask)

            # offset
            dh = 0
            dw = 0
            bg_roi = img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]

            # get target area
            bg_roi = bg_roi.astype(float)
            mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
            alpha = mask_inv.astype(float)/255
            alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
            # print("alpha size: ",alpha.shape)
            # print("bg_roi size: ",bg_roi.shape)
            bg = cv2.multiply(alpha, bg_roi)
            bg = bg.astype('uint8')

            cv2.imwrite("bg.jpg",bg)

            # get hat
            hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)
            cv2.imwrite("hat.jpg",hat)

            hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))
            # combine
            add_hat = cv2.add(bg,hat)
            # cv2.imshow("add_hat",add_hat) 

            # add back to org image
            img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat

            return img

def main(hatName,photoName):
    # load hat image. -1 means load rgba channels, rgb otherwise
    hat_img = cv2.imread(hatName,-1)
    
    # load photo
    img = cv2.imread(photoName)
    output = add_hat(img,hat_img)
    #save
    cv2.imwrite("output.jpg",output)
    
if __name__=='__main__':
    if len(sys.argv)<2:
        hatName='hat.png'
        photoName='person.jpg'
    else:
        hatName=sys.argv[1]
        photoName=sys.argv[2]
    main(hatName,photoName)

