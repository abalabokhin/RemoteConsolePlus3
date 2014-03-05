#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

class StreamsTreeNode(dict):
    def __init__(self):
        self._selected = False
        
class StreamsTree(object):
    def __init__(self):
        self._root = StreamsTreeNode()
        
    def IsEnabledStream(self, rawStreamName):
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._root
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = StreamsTreeNode()
            curNode = curNode[component]
        
        return True

    def GetTreeInJstreeFormat(self):
        return self.ConvertStreamsTreeNodeIntoJstreeNode(self._root, ['#'])

    def ConvertStreamsTreeNodeIntoJstreeNode(self, node, namesStack):
        jsNode = {}
        jsNode['id'] = "/".join(namesStack)
        if namesStack[-1] != "#" and len(node) > 0:
            jsNode['id'] += "#"
        jsNode['text'] = namesStack[-1]
        jsNode['state'] = {'selected':node._selected}

        children = []
        
        localRootNode = {}
        localRootNode['id'] = "/".join(namesStack)
        localRootNode['text'] = '.'
        localRootNode['state'] = {'selected':node._selected}
        if namesStack[-1] != "#" and len(node) > 0:
            children.append(localRootNode)
       
        for childName in node:
            children.append(self.ConvertStreamsTreeNodeIntoJstreeNode(node[childName], namesStack+[childName]))
        
        jsNode['children'] = children
        return jsNode
    
    def ClearSelectionRecursively(self, node):
        node._selected = False
        for childName in node:
            self.ClearSelectionRecursively(node[childName])
    
    def UpdateSelectionFromList(self, selectedNodes):
        self.ClearSelectionRecursively(self._root)
        
        for selectedNodeId in selectedNodes:
            if selectedNodeId[-1] == '#':
                continue
            pathComponents = selectedNodeId.split("/")[1:]

            curNode = self._root
            for component in pathComponents:
                curNode = curNode[component]
            
            curNode._selected = True
