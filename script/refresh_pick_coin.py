from impression.models import PickCoin

# 更新小组长pick币
PickCoin.objects.filter(key_user=True).update(pick_coin_num=40)

# 更新组员的pick币
PickCoin.objects.filter(key_user=False).update(pick_coin_num=20)
