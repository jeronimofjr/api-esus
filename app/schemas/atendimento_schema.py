from marshmallow import Schema, fields, validate, validates_schema, ValidationError, post_dump


class AtendimentoSchema(Schema):
    id = fields.Int()
    nome = fields.String()
    cpf = fields.String()
    cns = fields.String()
    data_atendimento = fields.String()
    nascimento = fields.String()
    condicao_saude = fields.String()
    unidade = fields.String()
    
    @post_dump
    def mask_sensitive_data(self, data, **kwargs):
        cpf = data.get("cpf")
        if cpf:
            data["cpf"] = f"***.***.***-{cpf[-2:]}"
        
        return data



class FiltrosAtendimentoSchema(Schema):
    
    data_atendimento = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$',
            error="Data deve estar no formato YYYY-MM-DD"
        ))
    
    unidade = fields.String(
        required=False, 
        allow_none=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"inválido" : "Unidade deve ser uma string válida"}
    )
    
    condicao_saude = fields.String(
        required=False,
        allow_none=True,
        validate=validate.OneOf(['hipertensao','diabetes','ferida vascular','dengue','tuberculose'],
                                error="Condição de saúde inválida. Valores aceitos: hipertensão, diabetes, ferida vascular, dengue ou tuberculose."),
    )
    
    page = fields.Int(
        required=False,
        load_default=1,
        validate=validate.Range(min=1)
    )

    limit = fields.Int(
        required=False,
        load_default=10,
        validate=validate.Range(min=1, max=100)
    )
    
    
class PeriodoAtendimentoSchema(Schema):

    data_inicio = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$',
            error="data_inicio deve estar no formato YYYY-MM-DD"
        )
    )

    data_fim = fields.String(
        required=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$',
            error="data_fim deve estar no formato YYYY-MM-DD"
        )
    )
    
    @validates_schema
    def validar_periodo(self, data, **kwargs):
        if data['data_inicio'] > data['data_fim']:
            raise ValidationError(
                "data_inicio não pode ser maior que data_fim",
                field_name="data_inicio"
            )