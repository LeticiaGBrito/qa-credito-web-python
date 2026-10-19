# Validação dos dados e regras de crédito

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ResultadoAnalise:
    status: str
    motivos: tuple[str, ...]


class AnaliseCreditoService:
    RENDA_MINIMA = Decimal("2000.00")
    MULTIPLICADOR_LIMITE = Decimal("5")

    def analisar(
        self,
        idade: int | None,
        renda_mensal: Decimal | None,
        valor_solicitado: Decimal | None,
    ) -> ResultadoAnalise:
        self._validar_dados(idade, renda_mensal, valor_solicitado)

        motivos = []

        if idade < 18:
            motivos.append(
                "Solicitante deve ter pelo menos 18 anos."
            )

        if renda_mensal < self.RENDA_MINIMA:
            motivos.append(
                "Renda mensal inferior a R$ 2.000,00."
            )

        if valor_solicitado > renda_mensal * self.MULTIPLICADOR_LIMITE:
            motivos.append(
                "Valor solicitado superior a cinco vezes a renda mensal."
            )

        status = "REPROVADO" if motivos else "APROVADO"

        return ResultadoAnalise(
            status=status,
            motivos=tuple(motivos),
        )

    def _validar_dados(
        self,
        idade: int | None,
        renda_mensal: Decimal | None,
        valor_solicitado: Decimal | None,
    ) -> None:
        if (
            idade is None
            or renda_mensal is None
            or valor_solicitado is None
        ):
            raise ValueError(
                "Idade, renda mensal e valor solicitado são obrigatórios."
            )

        # bool é um subtipo de int em Python; não deve ser aceito como idade.
        if type(idade) is not int or not 0 <= idade <= 120:
            raise ValueError(
                "Idade deve ser um número inteiro entre 0 e 120."
            )

        self._validar_valor_monetario(renda_mensal, "Renda mensal")
        self._validar_valor_monetario(valor_solicitado, "Valor solicitado")

    def _validar_valor_monetario(
        self,
        valor: Decimal,
        nome: str,
    ) -> None:
        if not isinstance(valor, Decimal):
            raise ValueError(
                f"{nome} deve ser informado como Decimal."
            )

        if not valor.is_finite():
            raise ValueError(
                f"{nome} deve ser um número finito."
            )

        if valor <= 0:
            raise ValueError(
                f"{nome} deve ser maior que zero."
            )

        if valor.as_tuple().exponent < -2:
            raise ValueError(
                f"{nome} deve ter no máximo duas casas decimais."
            )
