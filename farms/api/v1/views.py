from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Django
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Project
from farms.models import Farm, Log
from farms.serializers import FarmImageSerializer, FarmSerializer, LogImageSerializer, LogSerializer
from core.views import pagination


# 농장 리스트
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', FarmSerializer(many=True))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFarmList(request):
    '''
    농장(밭) 목록
    ---
    주인의 모든 농장(밭)을 보여주는 api 입니다.
    '''
    user = request.user
    farms = Farm.objects.filter(owner=user)
    page = request.query_params.get('page')
    paginator = Paginator(farms, 10)
    farms = pagination(page, paginator)
    serializer = FarmSerializer(farms, many=True)
    return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})


# 농장 한개 보기
@swagger_auto_schema(
    methods=['get'],
    responses={200: openapi.Response(
        'successfully patched', FarmSerializer(many=False))},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFarm(request, pk):
    '''
    농장 개별 보기
    ---
    pk를 통해 농장 한개의 정보를 가져옵니다.
    '''
    user = request.user
    farm = Farm.objects.get(id=pk)
    if farm.owner == user:
        serializer = FarmSerializer(farm, many=False)
        return Response({'result': serializer.data})
    else:
        message = {'detail': '농장을 찾을 수 없습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 농장 생성
@swagger_auto_schema(
    methods=['post'],
    responses={
        201: openapi.Response('successfully created', FarmSerializer),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postFarm(request):
    '''
    농장 생성
    ---
    이미지 업로드를 위해 생성을 클릭시 더미 데이터가 들어있는 농장을 만듭니다.
    이후 업데이트를 사용하여 농장을 생성하시면 됩니다.
    '''
    user = request.user
    try:
        farm = Farm.objects.create(
            title='Sample 농장',
            introduction='Sample',
            description='Description',
            owner=user,
        )
    except:
        message = {'detail': '입력하신 내용이 잘못되었습니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = FarmSerializer(farm, many=False)
    return Response(serializer.data)


# 농장 이미지
@swagger_auto_schema(
    methods=['post'],
    responses={
        201: openapi.Response('successfully created', FarmImageSerializer),
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadFarmImage(request, pk):
    '''
    농장 이미지 생성
    ---
    프론트 사용법
    ```
    const [image, setImage] = useState('')
    const uploadFileHandler = async (e) => {
        const file = e.target.files[0]
        const formData = new FormData()

        formData.append('image', file)
        formData.append('product_id', productId)

        setUploading(true)

        try {
            const config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }

            const { data } = await axios.post('/api/products/upload/', formData, config)


            setImage(data)
            setUploading(false)

        } catch (error) {
            setUploading(false)
        }
    } 
    ```
    '''
    data = request.data
    user = request.user
    pk = data['pk']
    farm = Farm.objects.get(id=pk)
    if farm.owner == user:
        farm.image = request.FILES.get('image')
        farm.save()
        serializer = FarmImageSerializer(farm, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '유저 정보가 다릅니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 농장 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("id", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="밭의 pk입니다."),
        ],
        required=['title', 'introduction', 'description'],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="밭의 이름"),
            'introduction': openapi.Schema(type=openapi.TYPE_STRING, description="밭의 정보"),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description="밭의 상세 정보"),
        },
    ),
    responses={
        200: openapi.Response('successfully created', FarmSerializer),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putFarm(request, pk):
    '''
    농장 수정하기
    ---
    전에 있던 내용을 넣어주시는 게 안전합니다.
    id는 밭의 pk입니다.
    '''
    user = request.user
    farm = Farm.objects.get(id=pk)
    data = request.data
    if farm.owner == user:
        farm.title = data["title"]
        farm.introduction = data["introduction"]
        farm.description = data["description"]
        farm.save()
        serializer = FarmSerializer(farm, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 농장 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteFarm(request, pk):
    '''
    농장 삭제
    ---
    농장의 pk로 삭제 합니다.
    '''
    user = request.user
    farm = Farm.objects.get(id=pk)
    if farm.owner == user:
        farm.delete()
    else:
        message = {'detail': '삭제 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    return Response('삭제 성공')


# 일지 리스트
@swagger_auto_schema(
    methods=['get'],
    responses={
        200: openapi.Response('successfully patched', LogSerializer(many=True))
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLogList(request, farm_pk):
    '''
    일지(log) 목록
    ---
    영농일지를 리스트로 볼수 있습니다.
    - 밭의 pk를 같이 보내야 합니다.(farm_pk)
    '''
    user = request.user
    try:
        farm = Farm.objects.get(id=farm_pk)
    except:
        return Response('farm does not exists')
    if user == farm.owner:
        logs = Log.objects.filter(farm_id=farm_pk)
        page = request.query_params.get('page')
        paginator = Paginator(logs, 10)
        logs = pagination(page, paginator)
        serializer = LogSerializer(logs, many=True)
        return Response({'result': serializer.data, 'page': page, 'pages': paginator.num_pages})
    else:
        message = {'detail': '일지 찾기 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 일지 한개 보기
@swagger_auto_schema(
    methods=['get'],
    responses={
        200: openapi.Response('successfully patched', LogSerializer)
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getLog(request, log_pk):
    '''
    일지 개별보기
    ---
    일지 pk (log_pk)를 같이 담아 보내야 합니다 
    '''
    user = request.user
    log = Log.objects.filter(owner=user, id=log_pk)
    serializer = LogSerializer(log, many=True)
    return Response({'result': serializer.data})


# 일지 생성
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("farm_pk", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="밭의 pk입니다."),
        ]
    ),
    responses={
        200: openapi.Response('successfully patched', LogSerializer)
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def postLog(request, farm_pk):
    '''
    일지 생성
    ---
    이미지 업로드를 위해 이 api를 먼저 호출 해주십쇼.더미데이터가 있는 일지를 생성하고 pk를 받아 옵니다.
    '''
    user = request.user
    farm = Farm.objects.get(id=farm_pk)
    try:
        if user == farm.owner:
            log = Log.objects.create(
                title="Sample 일지",
                content="일지 내용",
                worker="작업자",
                note="특이 사항",
                weather="맑음",
                farm=farm,
            )
    except:
        message = {'detail': '유저 정보가 잘못 되었습니다'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    serializer = LogSerializer(log, many=False)
    return Response(serializer.data)


# 일지 이미지
@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("log_pk", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="일지의 pk입니다."),
        ]
    ),
    responses={
        200: openapi.Response('successfully patched', LogImageSerializer)
    }
)
@api_view(['POST'])
def uploadLogImage(request, log_id):
    '''
    일지 이미지 생성
    ---
    '''
    data = request.data
    user = request.user
    log_id = data['log_id']
    log = Log.objects.get(id=log_id)
    if log.farm.owner == user:
        log.image = request.FILES.get('image')
        log.save()
        serializer = LogImageSerializer(log, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '유저 정보가 다릅니다.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 일지 수정
@swagger_auto_schema(
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        manual_parameters=[
            openapi.Parameter("log_pk", openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="일지의 pk입니다."),
        ],
        properties={
            'title': openapi.Schema(type=openapi.TYPE_STRING, description="제목"),
            'content': openapi.Schema(type=openapi.TYPE_STRING, description="내용"),
            'worker': openapi.Schema(type=openapi.TYPE_STRING, description="작업자"),
            'note': openapi.Schema(type=openapi.TYPE_STRING, description="특이사항"),
            'weather': openapi.Schema(type=openapi.TYPE_STRING, description="날씨"),
        },
    ),
    responses={
        200: openapi.Response('successfully patched')
    }
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def putLog(request, log_pk):
    '''
    일지 수정
    ---
    '''
    user = request.user
    log = Log.objects.get(id=log_pk)
    farm = log.farm
    data = request.data
    if farm.owner == user:
        log.title = data['title']
        log.content = data["content"]
        log.worker = data['worker']
        log.note = data['note']
        log.weather = data['weather']
        log.save()
        serializer = LogSerializer(log, many=False)
        return Response(serializer.data)
    else:
        message = {'detail': '수정 실패'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


# 일지 삭제
@swagger_auto_schema(
    methods=['delete'],
    responses={
        200: openapi.Response('successfully deleted')
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteLog(request, log_pk):
    '''
    일지 삭제
    ---
    '''
    user = request.user
    log = Log.objects.get(id=log_pk)
    owner = log.farm.owner
    if owner == user:
        log.delete()
    else:
        return Response('삭제 실패')
    return Response('삭제 성공')
