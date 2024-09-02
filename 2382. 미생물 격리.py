def number_of_microbiome(N, M, K, mc_map):
    # 상 하 좌 우
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    # 초기 군집 정보 설정
    for _ in range(M):
        # 각 시간마다의 이동을 처리
        new_map = {}

        for i in range(len(mc_map)):
            x, y, microbes, direction = mc_map[i]
            # 새로운 위치로 이동
            nx, ny = x + dx[direction - 1], y + dy[direction - 1]

            # 약품이 칠해진 셀에 도착한 경우
            if nx == 0 or nx == N - 1 or ny == 0 or ny == N - 1:
                microbes //= 2  # 미생물 수 절반으로 감소
                direction = direction - 1 if direction % 2 == 0 else direction + 1  # 방향 반전

            # 군집이 사라진 경우 (미생물 수가 0이 된 경우)
            if microbes == 0:
                continue

            # 새로운 위치에 이미 다른 군집이 있는 경우 합침
            if (nx, ny) in new_map:
                new_map[(nx, ny)].append((microbes, direction))
            else:
                new_map[(nx, ny)] = [(microbes, direction)]

        # 병합 후 새로운 상태 업데이트
        mc_map = []
        for key, value in new_map.items():
            if len(value) > 1:  # 여러 군집이 모인 경우
                # 미생물 수가 가장 많은 방향으로 합쳐짐
                total_microbes = sum(v[0] for v in value)
                max_microbes, max_direction = max(value)
                mc_map.append([key[0], key[1], total_microbes, max_direction])
            else:
                mc_map.append([key[0], key[1], value[0][0], value[0][1]])

    # M 시간이 지난 후 남아 있는 모든 미생물 수의 합 계산
    return sum(group[2] for group in mc_map)


T = int(input())
for tc in range(1, T + 1):
    # N: 정사각형 크기, M: 시간, K: 군집 개수
    N, M, K = map(int, input().split())
    micro_map = []
    for _ in range(K):
        micro_map.append(list(map(int, input().split())))

    result = number_of_microbiome(N, M, K, micro_map)
    print(f"#{tc} {result}")
