import cv2
import datetime
import time

interval=2
creds=[]

with open("aws-creds.txt") as f:
    for line in f:
        creds.append(line[:-1])

def uploadFile(fileName):
    from boto3.session import Session

    session = Session(aws_access_key_id=creds[0],
                      aws_secret_access_key=creds[1],
                      region_name='ap-northeast-1')
    s3 = session.resource("s3")
    bucket = s3.Bucket("human-rek")

    #test download
    bucket.upload_file(fileName, fileName)

################  Main Starts ###############################

while True:
    startTime=datetime.datetime.now()

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24.0, (640,480))

    while(datetime.datetime.now() - startTime < datetime.timedelta(0,interval)):
        ret, frame = cap.read()
        if ret==True:
            # write the flipped frame
            out.write(frame)

            # show window on screen
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()

    # time to do S3 upload
    uploadFile("output.mp4")

    time.sleep(3)
