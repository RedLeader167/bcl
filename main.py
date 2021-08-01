import sys, os
import ex
import bclparser
import bclpostparse
import bclinterpreter


throw = ex.throw

if len(sys.argv) < 2: throw(2)
if not os.path.isfile(sys.argv[1]): throw(1)

code = open(sys.argv[1]).read()

parser = bclparser.Parser(code)
res = parser.parse()

if res.state.ise(): throw(res.state.id, details="Error at line " + str(res.state.line + 1))

#print(res.tokens)

pparser = bclpostparse.PostParser(res.tokens)
res = pparser.parse()

if res.state.ise(): throw(res.state.id, details="Error at line " + str(res.state.line + 1))

#print("\n".join([str(i) for i in res.tokens[0]]))

#print("\n".join([str(i) for i in res.tokens[1]]))

intr = bclinterpreter.Interpreter(res.tokens[0], res.tokens[1], throw)
intr.executepre()
intr.reinit(res.tokens[0], res.tokens[1])
intr.execute()