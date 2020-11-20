import boto3
import json

def start_celebrity_rec():
    client = boto3.client('rekognition')
    response = client.start_celebrity_recognition(Video={'Bucket': 'cc-ex03-bucket-2', 'Name': 'example_sample.mp4'})
    startJobId = response['JobId']
    print('Start JobId : ' + startJobId)

    return startJobId

def recognize_celebrities(photo):
    name = ''
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.recognize_celebrities(Image={'Bytes': image.read()})

    print('Detected faces for ' + photo)
    for celebrity in response['CelebrityFaces']:
        name = celebrity['Name']

    return name

celebrities = [[], [], [], [], [], [], [], []] # 찾은 유명인사 리스트
cel_index1 = 0 # celebrities 리스트 인덱스1
cel_index2 = 0 # celebrities 리스트 인덱스2
contents = [] # s3에 있는 버킷에 있는 영상 자료 이름 리스트
con_index = 0 # contents 리스트 인덱스
search_bool = False # input으로 준 연예인이 존재했는가? 찾으면 True로 변환
photo = 'user_input.jpg' # 사용자가 찾고 싶은 연예인 이 연예인의 컨텐츠를 찾아보자

f = open('db.txt', 'r')
name = recognize_celebrities(photo)
job_id = start_celebrity_rec()
response = client.get_celebrity_recognition(job_id)

for celebrityRecognition in response['Celebrities']:
    celebrity[0].append(str(celebrityRecognition['Celebrity']['Name']))

for celebrity in celebrities:
    for cel_name in celebrity:
        if cel_name == name:
            search_bool = True
            break;
## 아직 미구현 아래는 db.txt에 있는 내용을 서치해
## 해당 연예인과 매칭되는 프로그램 리스트를 찾아내고 해당 리스트를 출력하고
## 프로그램들 끼리의 평점을 비교해 가장 좋은 것을 추천해주는 출력문 작
#if search_bool:
    #line_num = 0
    #lines = f.readlines()
    #for line in lines:
        #if (lines == contents[con_index]):
            #print("recommendation : ", )

