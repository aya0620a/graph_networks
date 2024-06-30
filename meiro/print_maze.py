#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 Hiroki Yano <yano@kwansei.ac.jp>
# All rights reserved.
#
# This software is released under the MIT License, see LICENSE.txt.
#

import networkx as nx
import matplotlib.pyplot as plt
import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()

    if sys.stdin.isatty():
        parser.add_argument("file", help="please set input file", type=str)

    parser.add_argument("--answer", help="optional", action="store_true")

    args = parser.parse_args()
    return(args)


def remove_frame(s,t,pair_list):
    for i in [s,t]:
        if i%n==0:
            x = (0,m-int(i/n))
            y = (0,m-int(i/n+1))
        elif i%n==n-1:
            x = (n,m-int(i/n))
            y = (n,m-int(i/n+1))
        elif int(i/n)==0:
            x = (i%n,m)
            y = (i%n+1,m)
        elif int(i/n)==m-1:
            x = (i%n,0)
            y = (i%n+1,0)
        else:
            continue
        pair = tuple([x,y])
        pair_list.append(pair)


def link2pair(a,b,pair_list):
    if int(b)==a+1 or int(b)==a+n:
        if int(b)==a+1:
            x = (b%n,m-int(a/n))
            y = (b%n,m-int(a/n+1))
        elif int(b)==a+n:
            x = (a%n,m-int(b/n))
            y = (a%n+1,m-int(b/n))
        pair = tuple([x,y])
        pair_list.append(pair)
    elif int(b)==a-1 or int(b)==a-n:
        link2pair(b,a,pair_list)


def print_answer(s,t,link_list):
    gp_ans = nx.Graph()
    gp_ans.add_nodes_from(list(range(m*n)))
    gp_ans.add_edges_from(link_list)
    shortest_path = nx.shortest_path(gp_ans, source=s, target=t)
    print("\nanswer_path:",shortest_path)
    nx.draw_networkx_nodes(gp_ans,pos=list((i%n+0.5, m-int(i/n)-0.5) for i in gp_ans.nodes()),nodelist=shortest_path,node_size=4900/m,node_color='r',node_shape=',')


def main():
    global m,n
    pair_list = []

    args = get_args()

    # input
    if hasattr(args, 'file'):
        f = open(args.file, "r", encoding="utf_8")
        m, n = map(int, f.readline().split(','))
        s, t = map(int, f.readline().split(','))
        N = int(f.readline())
        try:
            link_list = [tuple(list(map(int, line.split(',')))) for line in f.read().split('\n')]
        except ValueError:
            print("Error: blank line in the input file")
            sys.exit(1)
    else:
        print('m,n >> ',end='')
        m, n = map(int, input().split(','))
        print('s,t >> ',end='')
        s, t = map(int, input().split(','))
        print('N >> ',end='')
        N = int(input())
        link_list = [tuple(list(map(int, input().split(',')))) for i in range(N)]

    mgrid = m + 1
    ngrid = n + 1

    for i in range(N):
        link2pair(link_list[i][0],link_list[i][1],pair_list) 
    remove_frame(s,t,pair_list)

    if args.answer:
        print_answer(s,t,link_list)

    # graph
    gp = nx.grid_2d_graph(ngrid, mgrid)
    gp.remove_edges_from(pair_list)

    # draw
    nx.draw(gp,pos=dict((i, i) for i in gp.nodes()),node_size=0)
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    main()