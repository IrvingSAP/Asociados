# Generated by Django 5.1.1 on 2024-10-16 02:24

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaestroAsociado',
            fields=[
                ('id_asociado', models.AutoField(primary_key=True, serialize=False, verbose_name='ID socio')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre Asociado')),
                ('telefono', models.CharField(max_length=20, verbose_name='Telefono Asociado')),
                ('correo', models.CharField(max_length=50, verbose_name='Correo Asociado')),
                ('estado', models.CharField(max_length=1, verbose_name='Estado Asociado')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoCaja',
            fields=[
                ('id_CajaM', models.AutoField(primary_key=True, serialize=False, verbose_name='ID socio')),
                ('yymm_Caja', models.CharField(max_length=7, verbose_name='YYYY-MM')),
                ('fec_RegistroN', models.IntegerField(verbose_name='FecReg AAMMDD')),
                ('fec_Registro', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('id_Asociado', models.PositiveSmallIntegerField(verbose_name='ID Asociado')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre Asociado')),
                ('cod_Prestamo', models.PositiveSmallIntegerField(verbose_name='Codigo Prestamo')),
                ('sec_Caja', models.PositiveSmallIntegerField(verbose_name='Secuencia Prestamo')),
                ('accion_Caja', models.CharField(max_length=20, verbose_name='Accion')),
                ('motivo_Caja', models.CharField(max_length=20, verbose_name='Motivo')),
                ('fec_AplicaN', models.IntegerField(verbose_name='FecApl AAMMDD')),
                ('fec_Aplica', models.DateField(verbose_name='Fecha de Aplica')),
                ('monto_Aplica', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Monto Aplica')),
                ('s_Acumulado', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Acumulado')),
                ('observacion_Caja', models.CharField(max_length=100, verbose_name='Observacion')),
                ('tipo_Motivo', models.CharField(max_length=10, verbose_name='Tipo Motivo')),
            ],
        ),
        migrations.CreateModel(
            name='PrestamoAsociado',
            fields=[
                ('id_asociado', models.PositiveSmallIntegerField(primary_key=True, serialize=False, verbose_name='ID Caja')),
                ('cantPrestamos', models.IntegerField(verbose_name='Cantidad Prestamos')),
                ('actPrestamos', models.IntegerField(verbose_name='Prestamos Activos')),
                ('inacPrestamos', models.IntegerField(verbose_name='Prestamos Inactivos')),
                ('mayPrestamos', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Mayor Prestamo')),
                ('ultPrestamo', models.DateField(verbose_name='Ultimo Prestamo')),
                ('saldoPrestamo', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Saldo Socio')),
                ('estado', models.CharField(max_length=1, verbose_name='Estado Asociado')),
            ],
        ),
        migrations.CreateModel(
            name='PrestamosMovimiento',
            fields=[
                ('id_MP', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Mov Prestamo')),
                ('yymm_MP', models.CharField(max_length=7, verbose_name='YYYY-MM')),
                ('fec_RegistroN', models.IntegerField(verbose_name='FecReg AAMMDD')),
                ('fec_Registro', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('id_Asociado', models.PositiveSmallIntegerField(verbose_name='ID Asociado')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre Asociado')),
                ('cod_Prestamo', models.PositiveSmallIntegerField(verbose_name='Codigo Prestamo')),
                ('monto_Prestamo', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Monto Prestamo')),
                ('fec_IniN', models.IntegerField(verbose_name='FecIni AAMMDD')),
                ('fec_Ini', models.DateField(verbose_name='Fecha Inicial')),
                ('fec_FinN', models.IntegerField(verbose_name='FecFin AAMMDD')),
                ('fec_Fin', models.DateField(verbose_name='Fecha Final')),
                ('tasa_Int', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Tasa Int')),
                ('dias_cal', models.IntegerField(verbose_name='Dias Cal')),
                ('int_cal', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Int Cal')),
                ('fec_Pag_RegN', models.IntegerField(verbose_name='FecPagoReg AAMMDD')),
                ('fec_Pag_reg', models.DateField(auto_now_add=True, verbose_name='Fec Pago Registro')),
                ('fec_Pag_efeN', models.IntegerField(verbose_name='FecPagEfe AAMMDD')),
                ('fec_Pag_efe', models.DateField(null=True, verbose_name='Fec Pago Efectivo')),
                ('dias_cal_Pag', models.IntegerField(verbose_name='Dias Cal Pago')),
                ('int_cal_Pag', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Int Cal Pago')),
                ('int_01', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Int 01')),
                ('int_02', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Int 02')),
                ('abono_cap', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Abono Cap')),
                ('monto_pag', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Monto Pagado')),
                ('sal_pendiente', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Saldo Pendiente')),
                ('estado_reg', models.CharField(max_length=20, verbose_name='Estado Registro')),
                ('estado_prest', models.CharField(max_length=20, verbose_name='Estado Prestamo')),
                ('Form_pago', models.CharField(max_length=20, verbose_name='Forma Pago')),
                ('Observacion', models.CharField(max_length=100, verbose_name='Observacion')),
            ],
        ),
        migrations.CreateModel(
            name='SaldoCaja',
            fields=[
                ('id_Caja', models.AutoField(primary_key=True, serialize=False, verbose_name='ID socio')),
                ('estadoCaja', models.CharField(max_length=1, verbose_name='Estado Caja')),
                ('yymmCaja', models.CharField(max_length=7, verbose_name='YYYY-MM')),
                ('salIniCaja', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Sald Ini Caja')),
                ('entradaCaja', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Entrada Caja')),
                ('salidaCaja', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Salida Caja')),
                ('salFinCaja', models.FloatField(validators=[core.models.validate_decimals], verbose_name='Sald Fin Caja')),
            ],
        ),
        migrations.CreateModel(
            name='TablaSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_Sistema', models.CharField(max_length=6, verbose_name='Codgio Sistema')),
                ('Valor_Sistema', models.CharField(max_length=10, verbose_name='Valor de Sistema')),
                ('desc_Valor', models.CharField(max_length=50, verbose_name='Descripcion Valor')),
            ],
        ),
    ]