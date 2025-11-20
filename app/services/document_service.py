# app/services/document_service.py

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
from app.models.models import User, Payment, PaymentStatus


class DocumentService:

    def gerar_recibo_pdf(self, payment: Payment, user: User) -> bytes:
        """
        Gera um PDF de Recibo para um pagamento APROVADO.
        Retorna os bytes do arquivo PDF.
        """
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Cabeçalho
        c.setFont("Helvetica-Bold", 20)
        c.drawString(2 * cm, 28 * cm, "AVAMUD - Recibo de Pagamento")

        c.setFont("Helvetica", 12)
        c.drawString(2 * cm, 27 * cm, f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        c.line(2 * cm, 26.5 * cm, 19 * cm, 26.5 * cm)

        # Corpo do Recibo
        c.setFont("Helvetica", 14)
        textos = [
            f"Código do Pagamento: #{payment.id}",
            f"Pagador: {user.nome}",
            f"CPF: {user.cpf}",
            f"Valor Pago: R$ {payment.valor:.2f}",
            f"Data do Vencimento: {payment.data_vencimento.strftime('%d/%m/%Y')}",
            f"Status: {payment.status.value}",
            f"Forma de Pagamento: {payment.forma_pagamento.value if hasattr(payment, 'forma_pagamento') else 'N/A'}"
        ]

        y = 24
        for linha in textos:
            c.drawString(2 * cm, y * cm, linha)
            y -= 1

        # Rodapé
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(2 * cm, 4 * cm, "Este documento comprova a quitação do débito acima descrito.")
        c.drawString(2 * cm, 3.5 * cm, "Associação dos Vendedores Ambulantes do Município de Diamantina.")

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer.getvalue()

    def gerar_declaracao_regularidade(self, user: User) -> bytes:
        """
        Gera um PDF declarando que o membro está ativo.
        """
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Título
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(10.5 * cm, 25 * cm, "DECLARAÇÃO DE REGULARIDADE")

        # Texto
        texto_corpo = f"""
        Declaramos para os devidos fins que o associado(a) {user.nome},
        inscrito(a) no CPF sob o nº {user.cpf}, encontra-se devidamente
        CADASTRADO e ATIVO no quadro de membros da AVAMUD
        (Associação dos Vendedores Ambulantes do Município de Diamantina).
        """

        c.setFont("Helvetica", 12)
        text_object = c.beginText(2 * cm, 20 * cm)
        for line in texto_corpo.split("\n"):
            text_object.textLine(line.strip())
        c.drawText(text_object)

        # Data e Assinatura
        c.drawString(2 * cm, 15 * cm, f"Diamantina, {datetime.now().strftime('%d de %B de %Y')}.")

        c.line(6 * cm, 10 * cm, 15 * cm, 10 * cm)
        c.drawCentredString(10.5 * cm, 9.5 * cm, "Presidência / Tesouraria AVAMUD")

        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer.getvalue()