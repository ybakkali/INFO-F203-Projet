def hierarchy_pos(G, root, width=1, vert_gap = 0.2, vert_loc = 0, xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    print(neighbors)
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx+0.075, vert_gap = vert_gap,
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent = root)
    return pos

    def show(self,figure,title,x_offset=0):
        G1 = nx.DiGraph()
        pos = self.makeGraph(G1,x_offset)
        plt.figure(figure,figsize=(20,10))
        temp = pos[self.getNodeName()]
        plt.text(temp[0],temp[1]+0.02,title,horizontalalignment="center",fontsize=20)
        nx.draw_networkx_nodes(G1,pos,node_size=650,node_color='red',alpha=0.5)
        nx.draw_networkx_edges(G1,pos,width=2,arrowstyle="-|>",arrowsize=15,edge_color='blue',alpha=0.25)
        nx.draw_networkx_labels(G1,pos,font_size=10,font_family='sans-serif',font_color='black')
        plt.axis('off')

    def makeGraph(self, G, pos = {}, x = 0.5, y = 0, space = 0.2, width = 1):

        pos[self.getNodeName()] = (x,y)

        if len(self.children) != 0:

            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                G.add_edge(self.getNodeName(),child.getNodeName())
                nx += dx
                pos = child.makeGraph(G,pos,nx,y-space,space,dx+0.075)

        return pos


        def makeGraph(self, G, x_offset = 0, pos = {}, x = 0.5, y = 0, space = 0.2, width = 1):

        pos[self.getNodeName()] = (x+x_offset,y)

        if len(self.children) != 0:

            dx = width/len(self.children)
            nx = x - width/2 - dx/2

            for child in self.children:
                G.add_edge(self.getNodeName(),child.getNodeName())
                nx += dx
                pos = child.makeGraph(G,x_offset,pos,nx,y-space,space,dx+0.075)

        return pos

#test
#hi
