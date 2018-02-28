#上下文渲染器
from my_app.models import *
def Column(request):
    cilckatr=Article.objects.all().order_by('-numcilck')[:10]
    Recommend=Article.objects.all().order_by('-weight')[:10]
    return {'Colatr':cilckatr,'Recom':Recommend,'usname':request.session.get('name')}
