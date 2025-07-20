from SimpleLangVisitor import SimpleLangVisitor
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):
    def __init__(self):
        self.errors = []
        self.types = {}

    def visitProg(self, ctx: SimpleLangParser.ProgContext):
        for stat in ctx.stat():
            self.visit(stat)
        
        if self.errors:
            raise TypeError("\n".join(self.errors))  # Lanzamos una excepción con todos los errores
        return None

    def visitStat(self, ctx: SimpleLangParser.StatContext):
        t = self.visit(ctx.expr())
        self.types[ctx] = t
        return t

    def visitInt(self, ctx: SimpleLangParser.IntContext):
        t = IntType()
        self.types[ctx] = t
        return t

    def visitFloat(self, ctx: SimpleLangParser.FloatContext):
        t = FloatType()
        self.types[ctx] = t
        return t

    def visitString(self, ctx: SimpleLangParser.StringContext):
        t = StringType()
        self.types[ctx] = t
        return t

    def visitBool(self, ctx: SimpleLangParser.BoolContext):
        t = BoolType()
        self.types[ctx] = t
        return t

    def visitParens(self, ctx: SimpleLangParser.ParensContext):
        t = self.visit(ctx.expr())
        self.types[ctx] = t
        return t

    def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op    = ctx.op.text
        if isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
            t = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            t = "error"
        self.types[ctx] = t
        return t

    def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op    = ctx.op.text
        if op == '+' and isinstance(left, StringType) and isinstance(right, StringType):
            t = StringType()
        elif isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
            t = FloatType() if isinstance(left, FloatType) or isinstance(right, FloatType) else IntType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            t = "error"
        self.types[ctx] = t
        return t

    def visitRelationalExpr(self, ctx: SimpleLangParser.RelationalExprContext):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op    = ctx.op.text
        if isinstance(left, (IntType, FloatType)) and isinstance(right, (IntType, FloatType)):
            t = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            t = "error"
        self.types[ctx] = t
        return t

    def visitEqualityExpr(self, ctx: SimpleLangParser.EqualityExprContext):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op    = ctx.op.text
        if type(left) == type(right):
            t = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            t = "error"
        self.types[ctx] = t
        return t

    def visitLogicalExpr(self, ctx: SimpleLangParser.LogicalExprContext):
        left  = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op    = ctx.op.text
        if isinstance(left, BoolType) and isinstance(right, BoolType):
            t = BoolType()
        else:
            self.errors.append(f"Unsupported operand types for {op}: {left} and {right}")
            t = "error"
        self.types[ctx] = t
        return t
