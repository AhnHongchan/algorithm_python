from itertools import product


def calculate_min_time(people, stair_info, stair_assign):
    times = [[], []]  # 각 계단에 도착하는 사람들의 도착 시간 리스트
    stair_lengths = [stair_info[0][2], stair_info[1][2]]  # 계단의 길이 저장

    # 각 사람이 어느 계단을 사용할 지에 따라 도착 시간을 계산
    # 인덱스와 원소를 enumerate를 통해 받을 수 있음
    for i, assign in enumerate(stair_assign):
        px, py = people[i]
        sx, sy, _ = stair_info[assign]
        arrival_time = abs(px - sx) + abs(py - sy)
        times[assign].append(arrival_time)

    max_time = 0
    # 각 계단별로 시간을 계산
    for stair_index in range(2):
        times[stair_index].sort()
        stair_queue = []
        current_time = 0

        for arrival in times[stair_index]:
            # 계단 입구에 도착하면 1분 대기 후 계단을 내려가야 하므로 +1 추가
            arrival += 1

            if arrival > current_time:
                # 계단에서 내려간 시간 중 최대값으로 업데이트
                current_time = arrival
            # 현재 시간에 내려가는 사람 추가
            while stair_queue and stair_queue[0] <= current_time:
                stair_queue.pop(0)

            if len(stair_queue) < 3:  # 계단에 올라갈 수 있는 여유가 있는 경우
                stair_queue.append(current_time + stair_lengths[stair_index])
            else:  # 계단이 꽉 찬 경우
                next_available_time = stair_queue.pop(0)
                stair_queue.append(next_available_time + stair_lengths[stair_index])
                current_time = next_available_time

        if stair_queue:
            max_time = max(max_time, max(stair_queue))

    return max_time


def lunch_time(n, lunch):
    people = []
    stairs = []

    # 지도 정보 처리
    for x in range(n):
        for y in range(n):
            val = lunch[x][y]
            if val == 1:
                people.append((x, y))
            elif val > 1:
                stairs.append((x, y, val))

    min_time = float('inf')
    num_people = len(people)

    # 모든 사람들의 계단 선택 조합 생성
    for stair_assign in product([0, 1], repeat=num_people):
        current_time = calculate_min_time(people, stairs, stair_assign)
        min_time = min(min_time, current_time)

    return min_time


# 테스트 케이스 입력 처리
case = int(input())

for tc in range(1, case + 1):
    n = int(input())
    lunch_map = []
    for i in range(n):
        lunch_map.append(list(map(int, input().split())))

    # 결과 계산 및 출력
    result = lunch_time(n, lunch_map)
    print(f"#{tc} {result}")
