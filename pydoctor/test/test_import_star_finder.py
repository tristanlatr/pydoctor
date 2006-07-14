from compiler.visitor import walk
from compiler.transformer import parse
from pydoctor import model, astbuilder
from pydoctor.test.test_packages import processPackage
import py

def test_simple():
    system = model.System()
    builder = astbuilder.ASTBuilder(system)
    isf = astbuilder.ImportStarFinder(builder, 'bar')
    walk(parse("from foo import *"), isf)
    assert len(system.importstargraph) == 1
    edge, = system.importstargraph.iteritems()
    assert edge == ('bar', ['foo'])

def test_actual():
    system = processPackage("importstartest")
    cls = system.allobjects['importstartest.mod1.C']
    assert cls.bases == ['importstartest.mod2.B']
