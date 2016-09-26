


def calculate(tree,k,n):

    if(tree.getLeft() != None):
        calculate(tree.getLeft(),k,n)

    if(tree.getRight() != None):
        calculate(tree.getRight(),k,n)

    for i in range(0, (k+1)):
        for w in range(0, ((k*n)+1)):
            for s in range(0, (2+1)):
                if(tree.getBagType() == BagType.L):
                    pass
                if(tree.getBagType() == BagType.IV):
                    pass
                if(tree.getBagType() == BagType.IE):
                    pass
                if(tree.getBagType() == BagType.F):
                    pass
                if(tree.getBagType() == BagType.J):
                    pass
                if(tree.getBagType() == BagType.R):
                    pass
