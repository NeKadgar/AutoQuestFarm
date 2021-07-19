from heapq import *
from DB.PointsDB import add_point, get_location_points, get_near_points, get_point_by_id
from Path.PlayerDirection import distance_to

graph = {'A': [(2, 'M'), (3, 'P')],
         'M': [(2, 'A'), (2, 'N')],
         'N': [(2, 'M'), (2, 'B')],
         'P': [(3, 'A'), (4, 'B')],
         'B': [(4, 'P'), (2, 'N')]}


class Graph:
    graph = {}

    def __init__(self, location):
        points = get_location_points(location)
        for point in points:
            near = get_near_points(location, point.x, point.y, 40)
            near = [item for item in near if item.id != point.id]
            near_ = []
            for p in near:
                near_.append((distance_to(p, point), p.id))
            self.graph.update({point.id: near_})


def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                heappush(queue, (new_cost, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


def find_path(location, p_start, p_goal):
    points = get_location_points(location)
    start = min(points, key=lambda x: distance_to(x, p_start))
    goal = min(points, key=lambda x: distance_to(x, p_goal))
    visited = dijkstra(start.id, goal.id, Graph(location).graph)

    cur_node = goal.id
    way_id = []
    while cur_node != start.id:
        cur_node = visited[cur_node]
        way_id.append(cur_node)
    way = []
    for p in way_id:
        way.append(get_point_by_id(p))
    return reversed(way)
