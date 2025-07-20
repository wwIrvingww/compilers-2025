from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

    def __init__(self):
        self.errors = []
        self.types = {}

    def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        left  = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op    = ctx.op.text
        if not self.is_valid_arithmetic_operation(left, right):
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            self.types[ctx] = "error"
        else:
            self.types[ctx] = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

    def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        left  = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op    = ctx.op.text

        # string + string ➞ concatenación
        if op == '+' and isinstance(left, StringType) and isinstance(right, StringType):
            self.types[ctx] = StringType()

        elif self.is_valid_arithmetic_operation(left, right):
            self.types[ctx] = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()

        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            self.types[ctx] = "error"

    def exitRelationalExpr(self, ctx: SimpleLangParser.RelationalExprContext):
        left  = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op    = ctx.op.text

        if isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            self.types[ctx] = "error"

    def exitEqualityExpr(self, ctx: SimpleLangParser.EqualityExprContext):
        left  = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op    = ctx.op.text

        if type(left) == type(right):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            self.types[ctx] = "error"

    def exitLogicalExpr(self, ctx: SimpleLangParser.LogicalExprContext):
        left  = self.types[ctx.expr(0)]
        right = self.types[ctx.expr(1)]
        op    = ctx.op.text

        if isinstance(left, BoolType) and isinstance(right, BoolType):
            self.types[ctx] = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            self.types[ctx] = "error"

    def enterInt(self, ctx: SimpleLangParser.IntContext):
        self.types[ctx] = IntType()

    def enterFloat(self, ctx: SimpleLangParser.FloatContext):
        self.types[ctx] = FloatType()

    def enterString(self, ctx: SimpleLangParser.StringContext):
        self.types[ctx] = StringType()

    def enterBool(self, ctx: SimpleLangParser.BoolContext):
        self.types[ctx] = BoolType()

    def exitParens(self, ctx: SimpleLangParser.ParensContext):
        self.types[ctx] = self.types[ctx.expr()]

    def is_valid_arithmetic_operation(self, left, right):
        return isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType))
