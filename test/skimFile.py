import uproot
import sys
import awkward as ak
import re


# Branches to drop 
slimOut = [".*Proton.*",".*PFCand_.*","PFCands_trkPt","PFCands_trkEta","PFCands_trkPhi"]

# Skims to apply per collection (i.e. only drop entries in the collection but keep events)
skimColls = {"PFCands": lambda x: skimPFCands(x)}

def skimPFCands(x):
    cut = abs(x.eta) < 2.5
    return x[cut]

# Skims to apply per event (i.e. drop the whole event if it doesn't pass
def skimEvents(tree):
    #print("Skim by HLT")
    #nprev = len(tree)
    #cutHLT = (tree["HLT_VBF_DiPFJet125_45_Mjj1050"] | tree["HLT_VBF_DiPFJet125_45_Mjj1200"])
    #print("%i/%i events selected"%(nprev, sum(cutHLT)))
    #return tree[cutHLT]
    return tree


def getTree(inp, tr, sk=None, skc=None, sl=None):
    branches = inp[tr].keys()
    collections = {}
    singletons  = []
    for var in branches:
        if slimOut:
            keep = True
            for s in slimOut:
                if re.match(s, var):
                    keep = False
                    break
            if not(keep): 
                #print("Will skip %s"%var)
                continue
        if "_" in var:
            short = var.split("_")[0]
            if short in collections:
                collections[short].append(var.replace(short + "_",""))
            else:
                collections[short] = [var.replace(short + "_","")]
        else:
            singletons.append(var)
    tree = inp[tr].arrays(branches)
    if sk:
        tree = sk(tree)
    czips = {}
    for short in collections:
        #print(short)
        czips[short] = ak.zip({name: tree[short + "_" + name] for name in collections[short]})
        if short in skc:
            czips[short] = skimColls[short](czips[short])
    szips = {v : tree[v] for v in singletons}
    allzips = {}
    for c in czips:
        allzips[c] = czips[c]
    for s in szips:
        allzips[s] = szips[s]
    return allzips
    
def skimFile(inp, out, sk=None, sl=None):
    with uproot.open(inp) as f:
        with uproot.recreate(out, compression=uproot.ZLIB(9)) as ufile:
            print("Getting Events...")
            ufile["Events"] = getTree(f, "Events", sk, sl)
            print("Getting LuminosityBlocks...")
            ufile["LuminosityBlocks"] = getTree(f, "LuminosityBlocks")
            print("Getting Runs...")
            ufile["Runs"] = getTree(f, "Runs")

skimFile(sys.argv[1], sys.argv[2], None, skimEvents, slimOut)
