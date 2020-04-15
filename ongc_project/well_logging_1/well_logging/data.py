import lasio 
import petropy as pt
import elementpath
import xml.etree.ElementTree as et
import os

def prettify(element, indent='  '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  # for child open
        if queue:
            element.tail = '\n' + indent * queue[0][0]  # for sibling open
        else:
            element.tail = '\n' + indent * (level-1)  # for parent close
        queue[0:0] = children

def xml_create(l_new):
    xml_doc=et.Element('graph',width="5",height="100")
    l_new.reverse()
    t_name=['TRACK_1','DEPTH','RESISTIVITY','NEUTRON DENSITY']
    color=["#cc0000","#006400","#000000","#FF0000","#0099CC","#ffdb58"]
    left=["140","0.45","1.95","1","0","6"]
    right=["40","-0.15","2.95","1000","150","24"]
    width=["2","1.5","0.5","1"]
    t_name.reverse()
    color.reverse()
    for i in range(0,4):
        j=t_name.pop()
        if j=='RESISTIVITY':
            track=et.SubElement(xml_doc,'track',display_name=j,scale="log",width=width.pop())
            k=l_new.pop()
            et.SubElement(track,'curve',display_name=k,curve_name=k,color=color.pop(),left=left.pop(),right=right.pop())
        elif j=='DEPTH':
            track=et.SubElement(xml_doc,'track',display_name=j,number_spacing="200",tick_spacing="10",line_spacing="50",width=width.pop())
        elif j=='NEUTRON DENSITY':
            track=et.SubElement(xml_doc,'track',display_name=j,width=width.pop(),major_lines="9")
            while(len(l_new)):
                k=l_new.pop()
                et.SubElement(track,'curve',display_name=k,curve_name=k,color=color.pop(),left=left.pop(),right=right.pop())
        else:
            track=et.SubElement(xml_doc,'track',display_name=j,width=width.pop(),major_lines="9")
            k=l_new.pop()
            et.SubElement(track,'curve',display_name=k,curve_name=k,color=color.pop(),left=left.pop(),right=right.pop())
            k=l_new.pop()
            et.SubElement(track,'curve',display_name=k,curve_name=k,color=color.pop(),left=left.pop(),right=right.pop())
    prettify(xml_doc)
    xml_path=os.path.abspath("well_logging/static/")
    xml_path=xml_path+"\\template"+str(i)+".xml"
    tree=et.ElementTree(xml_doc)
    tree.write(xml_path,encoding='UTF-8',xml_declaration=True)
    return xml_path

def data_process():     
    top=0
    height=0   
    for i in range(1,4):
        filepath=os.path.abspath("well_logging/static/B_"+str(i)+".las")
        ls=lasio.read(filepath)
        if top==0 and height==0:
            top=min(ls.depth_m)
            height=max(ls.depth_m)
        else:
            top=min(min(ls.depth_m),top)
            height=max(max(ls.depth_m),height)
    for i in range(1,4):
        filepath=os.path.abspath("well_logging/static/B_"+str(i)+".las")
        ls=lasio.read(filepath)
        l=['CALI','GR','SGR','LLD','RHOB','NPHI','DT']
        l_new=list()
        for j in l:
            if j in ls.curves:
                l_new.append(j)
        xml_path=xml_create(l_new)
        log=pt.Log(filepath)
        view= pt.LogViewer(log,top=top,height=height,template_xml_path=xml_path)
        s=os.path.abspath("well_logging/static/pictures/")
        s=s+"\img_"+str(i)+".png"
        view.fig.savefig(s)