import random
import game_explain
game_explain.game()
confirm = True
while confirm :
    cnt_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #카드 카운팅 리스트
    com_chip = 50 #플레이어1의 시작칩 개수
    user_chip = 50 #플레이어2의 시작칩 개수
    while True :
        bating = 0 #전체 배팅 칩 개수
        cnt = 0 #리셔플 판단 변수
        if com_chip <= 0 :
            print("\n플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
            print("상대방의 칩이 0개 이므로 플레이어의 승리입니다.")
            confirm = False
            break
        elif user_chip <= 0 :
            print("\n플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
            print("플레이어의 칩이 0개 이므로 상대방의 승리입니다.")
            confirm = False
            break
        for i in range(0, 10) :
            if cnt_list[i] == 2 :
                cnt += 1
        if cnt == 10 :
            print("카드를 전부다 소모했습니다. 새로운 카드로 이어서 게임을 진행하겠습니다.")
            for i in range(0, 10) :
                cnt_list[i] = 0
            continue
        #상대방 카드설정
        com_card = random.randint(1, 10)
        if cnt_list[com_card-1] == 2 :
            continue
        cnt_list[com_card-1] += 1
        #플레이어 카드설정
        user_card = random.randint(1, 10)
        if cnt_list[user_card-1] == 2 :
            continue
        cnt_list[user_card-1] += 1
        print("\n상대방 카드 :", com_card, "\t플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
        user_bating = int(input("배팅할 칩 개수를 입력하세요. : "))
        user_chip -= user_bating
        bating += user_bating
        act = random.randint(0, 3)
        if act == 0 : #컴퓨터가 콜만 했을 때
            com_bating = user_bating
            bating += com_bating
            com_chip -= com_bating
            print("\n상대방이 콜을 했고 추가 배팅은 없습니다.")
            print("배팅 칩 개수 :", bating, "\t플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
            print("\n카드를 오픈합니다.")
            print("플레이어 카드 :", user_card, "\t상대방 카드 :", com_card)
            if com_card > user_card :
                print("상대방의 승리입니다.")
                com_chip += bating
            elif user_card > com_card :
                print("플레이어의 승리입니다.")
                user_chip += bating
            else :
                print("무승부 입니다.")
                com_chip += com_bating
                user_chip += user_bating
        elif act == 1 : #컴퓨터가 추가 배팅 했을 때
            com_bating = user_bating + random.randint(1, 5)
            bating += com_bating
            com_chip -= com_bating
            print("\n상대방이 콜을 하고  추가 배팅을 했습니다. 콜 하시겠습니까?(0 : 콜, 1 : 추가 배팅, 2 : 포기)")
            print("배팅 칩 개수 :", bating, "\t플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
            user_act = int(input("입력 : "))
            if user_act == 0 : #플레이어가 콜 했을 때
                bating += com_bating
                user_chip -= com_bating
                print("\n플레이어가 콜을 했습니다.")
                print("배팅 칩 개수 :", bating, "\t플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
                print("\n카드를 오픈 합니다.")
                print("플레이어 카드 :", user_card, "\t상대방 카드 :", com_card)
                if com_card > user_card :
                    print("상대방의 승리입니다.")
                    com_chip += bating
                elif user_card > com_card :
                    print("플레이어의 승리입니다.")
                    user_chip += bating
                else :
                    print("무승부 입니다.")
                    com_chip += com_bating
                    user_chip += user_bating + com_bating
            elif user_act == 1 : #플레이어가 추가 배팅을 했을 때
                print("\n추가 배팅 선택 했습니다. ")
                add = int(input("추가 칩 개수 : "))
                bating += com_bating + add
                user_chip -= com_bating + add
                bating += add
                com_chip -= add
                print("상대방이 추가 배팅에 콜을 했습니다.")
                print("배팅 칩 개수 :", bating, "\t플레이어 칩 개수 :", user_chip, "\t상대방 칩 개수 :", com_chip)
                print("\n카드를 오픈합니다.")
                print("플레이어 카드 :", user_card, "\t상대방 카드 :", com_card)
                if com_card > user_card :
                    print("상대방의 승리입니다.")
                    com_chip += bating
                elif user_card > com_card :
                    print("플레이어의 승리입니다.")
                    user_chip += bating
                else :
                    print("무승부 입니다.")
                    com_chip += com_bating
                    user_chip += user_bating
            else : #플레이어가 포기 했을 때
                print("\n플레이어가 포기를 선언했습니다.")
                print("플레이어 카드 :", user_card, "\t상대방 카드 :", com_card)
                com_chip += bating
                if user_card == 10 :
                    print("플레이어가 숫자 10을 가지고 포기했습니다. 따라서 칩 10개를 지불합니다.")
                    com_chip += 10
                    user_chip -= 10
        else : #컴퓨터가 포기 했을 때
            print("\n상대방이 포기를 선언했습니다.")
            print("플레이어 카드 :", user_card, "\t상대방 카드 :", com_card)
            user_chip += bating
            if com_card == 10 :
                print("상대방이 숫자 10을 가지고 포기했습니다. 따라서 칩을 추가로 10개 받습니다.")
                user_chip += 10
                com_chip -= 10