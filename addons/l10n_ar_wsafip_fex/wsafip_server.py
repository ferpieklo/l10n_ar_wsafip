# -*- coding: utf-8 -*-
from openerp import models, api
from openerp.exceptions import Warning
import logging
from openerp.addons.l10n_ar_wsafip.tools import service, check_afip_errors

_logger = logging.getLogger(__name__)

logging.getLogger('suds.transport').setLevel(logging.DEBUG)

fex_service = service('wsfex')
fex_service_without_auth = service('wsfex', without_auth=True)

class wsafip_server(models.Model):
    _inherit = "wsafip.server"
    """
    Imprementación de Factura electrónica de exportación.

    Ref:
  https://www.afip.gob.ar/fe/documentos/WSFEX-Manualparaeldesarrollador_V1_1.pdf
    """

    @api.multi
    @fex_service
    def wsfex_autorize(self, service, auth, invoice):
        """
        2.1 Autorizador (FEXAuthorize)
        """
        response = service.FEXAuthorize(Auth=auth,
                                        Cmp=invoice)
        check_afip_errors(response)
        return response

    @api.multi
    @fex_service
    def wsfex_query_invoice(self, service, auth,
                            cbte_tipo, punto_vta, cbte_nro):
        """
        2.2 Recuperador de Comprobante (FEXGetCMP)
        """
        response = service.FEXGetCMP(Auth=auth,
                                     Cmp={'Cbte_Tipo': cbte_tipo,
                                          'Punto_vta': punto_vta,
                                          'Cbte_nro': cbte_nro})
        check_afip_errors(response)
        return response

    @api.multi
    @fex_service
    def wsfex_get_last_request_id(self, service, auth):
        """
        2.3 Recuperador de último valor de Id de requerimiento (FEXGetLast_ID)
        """
        response = service.FEXGetLast_ID(Auth=auth)
        check_afip_errors(response)
        return response

    @api.multi
    @fex_service
    def wsfex_get_last_invoice_number(self, service, auth):
        """
        2.4 Recuperador delúltimo Cbte_nroautorizado(FEXGetLast_CMP)
        """
        response = service.FEXGetLast_CMP(Auth=auth)
        check_afip_errors(response)
        return response

    @api.multi
    @fex_service
    def wsfex_get_currency_codes(self, service, auth):
        """
        2.5 Recuperador de valores referenciales de códigosde Moneda
        (FEXGetPARAM_MON)
        """
        response = service.FEXGetPARAM_MON(Auth=auth)
        check_afip_errors(response)
        return {
            r.Mon_Id: {
                'description': unicode(r.Mon_Ds).strip(),
                'date_from': r.Mon_vig_desde,
                'date_to': r.Mon_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_invoice_type_codes(self, service, auth):
        """
        2.6 Recuperador de valores referenciales de códigos de
        Tipos de comprobante (FEXGetPARAM_Cbte_Tipo)
        """
        response = service.FEXGetPARAM_Cbte_Tipo(Auth=auth)
        check_afip_errors(response)
        return {
            r.Cbte_Id: {
                'description': unicode(r.Cbte_Ds).strip(),
                'date_from': r.Cbte_vig_desde,
                'date_to': r.Cbte_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_export_type_codes(self, service, auth):
        """
        2.7 Recuperador de valores referenciales de códigos de
        Tipo de exportación (FEXGetPARAM_Tipo_Expo)
        """
        response = service.FEXGetPARAM_Tipo_Expo(Auth=auth)
        check_afip_errors(response)
        return {
            r.Tex_Id: {
                'description': unicode(r.Tex_Ds).strip(),
                'date_from': r.Tex_vig_desde,
                'date_to': r.Tex_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_unity_type_codes(self, service, auth):
        """
        2.8 Recuperador de valores referenciales de códigos de
        Unidades de Medida (FEXGetPARAM_UMed)
        """
        response = service.FEXGetPARAM_UMed(Auth=auth)
        check_afip_errors(response)
        return {
            r.Umed_Id: {
                'description': unicode(r.Umed_Ds).strip(),
                'date_from': r.Umed_vig_desde,
                'date_to': r.Umed_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_lang_codes(self, service, auth):
        """
        2.9 Recuperador de valores referenciales de códigos de
        Idiomas (FEXGetPARAM_Idiomas)
        """
        response = service.FEXGetPARAM_Idiomas(Auth=auth)
        check_afip_errors(response)
        return {
            r.Idi_Id: {
                'description': unicode(r.Idi_Ds).strip(),
                'date_from': r.Idi_vig_desde,
                'date_to': r.Idi_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_country_codes(self, service, auth):
        """
        2.10 Recuperador de valores referenciales de códigos de
        Países (FEXGetPARAM_DST_pais)
        """
        response = service.FEXGetPARAM_DST_pais(Auth=auth)
        check_afip_errors(response)
        return {
            r.DST_Codigo: unicode(r.DST_Ds).strip()
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_incoterms_codes(self, service, auth):
        """
        2.11 Recuperador de valores referenciales de
        Incoterms (FEXGetPARAM_Incoterms)
        """
        response = service.FEXGetPARAM_Incoterms(Auth=auth)
        check_afip_errors(response)
        return {
            r.Inc_Id: {
                'description': unicode(r.Inc_Ds).strip(),
                'date_from': r.Inc_vig_desde,
                'date_to': r.Inc_vig_hasta,
            }
            for r in response.FEXResultGet[0]
            if r is not None
        }

    @api.multi
    @fex_service
    def wsfex_get_country_cuit_codes(self, service, auth):
        """
        2.12 Recuperador de valores referenciales de CUITs de
        Países (FEXGetPARAM_DST_CUIT)
        """
        response = service.FEXGetPARAM_DST_CUIT(Auth=auth)
        if response.FEXErr.ErrCode != 0:
            raise Warning(response.FEXErr.ErrMsg)

        country = {}
        for result in response.FEXResultGet[0]:
            _c, _t = result.DST_Ds.split(' - ')
            if _c not in country:
                country[_c] = {}
            if _t not in country[_c]:
                country[_c][_t] = result.DST_CUIT
        return country

    @api.multi
    @fex_service
    def wsfex_get_currency_value(self, service, auth, mon_id):
        """
        2.13 Recuperador de cotizaciónde moneda (FEXGetPARAM_Ctz)
        """
        response = service.FEXGetPARAM_Ctz(Auth=auth, Mon_id=str(mon_id))
        if response.FEXErr.ErrCode != 0:
            return False

        return response.FEXResultGet.Mon_ctz, response.FEXResultGet.Mon_fecha

    @api.multi
    @fex_service
    def wsfex_get_web_points_of_sale(self, service, auth):
        """
        2.14 Recuperador de los puntos de venta asignados a
        Facturación Electrónica de comprobantes de Exportación vía
        Web Services (FEXGetPARAM_PtoVenta)
        """
        response = service.FEXGetPARAM_PtoVenta(Auth=auth)
        check_afip_errors(response)

        if not response.FEXResultGet:
            return {}

        return {
            r.Pve_Nro: {
                'unactive': r.Pve_Bloqueado,
                'date_to': r.Pve_FchBaja,
            }
            for r in response.FEXResultGet[0]
        }

    @api.multi
    @fex_service
    def wsfex_check_permissions(self, service, auth, id_permiso, dst_merc):
        """
        2.15 Verificador  de existencia de Permiso/País de destinación en
        bases de datos aduaneras (FEXCheck_Permiso)
        """
        response = service.FEXCheck_Permiso(Auth=auth,
                                            ID_Permiso=str(id_permiso),
                                            Dst_merc=int(dst_merc))
        return response

    @api.multi
    @fex_service_without_auth
    def wsfex_dummy(self, service):
        """
        2.16 MétodoDummy para verificación de funcionamiento de
        infraestructura (FEXDummy)
        """
        response = service.FEXDummy()

        if response.AuthServer != 'OK':
            raise Warning('Authentication is offline')
        if response.AppServer != 'OK':
            raise Warning('Webservice is offline')
        if response.DbServer != 'OK':
            raise Warning('Database is offline')

        return True

    @api.one
    def wsfex_update_countries(self, conn_id):
        country_cuit = self.wsfex_get_country_cuit_codes(conn_id)

        country_mod = self.env['res.country']

        CUIT_FISICA = u'Persona F\xedsica'
        CUIT_JURIDICA = u'Persona Jur\xeddica'
        CUIT_OTRO = u'Otro tipo de Entidad'
        cou_ignore = [
            'REPUBLICA',
            'ZONA',
            'LIBRE',
            'ARCHIPIELAGO',
            'DE',
            'ISLA',
            'ESTADOS',
        ]

        for cou in country_cuit:
            cuit_fisica = country_cuit[cou].get(CUIT_FISICA, False)
            cuit_juridica = country_cuit[cou].get(CUIT_JURIDICA, False)
            cuit_otro = country_cuit[cou].get(CUIT_OTRO, False)

            if not (cuit_fisica and cuit_juridica and cuit_otro):
                continue

            cou_names = [ c for c in cou.split(' ') if c not in cou_ignore ]
            country = country_mod.search(['|', '|', '|',
                ('cuit_fisica','=',cuit_fisica),
                ('cuit_juridica','=',cuit_juridica),
                ('cuit_otro','=',cuit_otro),
                ('name','in',cou_names),
            ])
            if not country:
                _logger.info('Can\'t find country name "%s"' % cou)
            elif len(country) == 1:
                country.write({
                    'cuit_fisica': cuit_fisica,
                    'cuit_juridica': cuit_juridica,
                    'cuit_otro': cuit_otro,
                })
            else:
                _logger.error('Multiple countries name "%s"' % cou)

    @api.one
    def wsfex_update_currencies(self, conn_id):
        currencies = self.wsfex_get_currency_codes(conn_id)

        currency_mod = self.env['res.currency']
        rate_mod = self.env['res.currency.rate']

        for cur in currencies:
            description = currencies[cur]['description']
            date_from = currencies[cur]['date_from']
            date_to = currencies[cur]['date_to']

            cur_obj = currency_mod.search([('afip_code','=',cur)])

            if cur_obj:
                _logger.info('Update currency %s' % cur)

                cur_obj.write({
                    'afip_desc': description,
                    'afip_dt_from': date_from,
                })

                rate = self.wsfex_get_currency_value(conn_id, cur)

                if rate and cur_obj.rate != rate[0]:
                    rate_mod.create({
                        'currency_id': cur_obj.id,
                        'rate': rate[0],
                        'create_date': rate[1],
                    })
                    _logger.info('Update rate to %s' % rate[0])

    @api.one
    def wsfex_update_invoice_type(self, conn_id):
        invoice_types = self.wsfex_get_invoice_type_codes(conn_id)

        template_mod = self.env['afip.journal_template']

        for ty in invoice_types:
            description = invoice_types[ty]['description']
            date_from = invoice_types[ty]['date_from']
            date_to = invoice_types[ty]['date_to']

            tem_obj = template_mod.search([('code', '=', ty)])

            if not tem_obj:
                template_mod.create({
                    'code': ty,
                    'name': description
                })
                _logger.info('Created template %s' % ty)

    @api.one
    def wsfex_update_export_type_codes(self, conn_id):
        export_types = self.wsfex_get_export_type_codes(conn_id)

        concept_mod = self.env['afip.concept_type']

        for ty in export_types:
            description = export_types[ty]['description']
            date_from = export_types[ty]['date_from']
            date_to = export_types[ty]['date_to']

            con_obj = concept_mod.search([('afip_code' ,'=', ty),'|',
                                          ('active', '=', False),
                                          ('active', '=', True)])

            if not con_obj:
                concept_mod.create({
                    'afip_code': ty,
                    'name': description,
                    'product_types': 'UNSET',
                    'active': True,
                })
                _logger.info('Created concept %s' % ty)
            else:
                con_obj.write({'active': True})

    @api.one
    def wsfex_update_units(self, conn_id):
        units = self.wsfex_get_unity_type_codes(conn_id)

        unit_mod = self.env['product.uom']

        for uom in units:
            description = units[uom]['description']
            date_from = units[uom]['date_from']
            date_to = units[uom]['date_to']

            uom_obj = unit_mod.search([('name', '=', description)])
            uom_obj.write({'afip_code': uom})

    @api.one
    def wsfex_update_languages(self, conn_id):
        langs = self.wsfex_get_lang_codes(conn_id)

        lang_mod = self.env['res.lang']

        for l in langs:
            description = langs[l]['description']
            date_from = langs[l]['date_from']
            date_to =  langs[l]['date_to']

            lang_obj = lang_mod.search([('name', '=', description)])
            lang_obj.write({'afip_code': l})

    @api.one
    def wsfex_update_incoterms(self, conn_id):
        incoterms = self.wsfex_get_incoterms_codes(conn_id)

        inco_mod = self.env['stock.incoterms']

        for i in incoterms:
            description = incoterms[i]['description']
            date_from = incoterms[i]['date_from']
            date_to = incoterms[i]['date_to']

            inco_obj = inco_mod.search([('name', '=', description)])
            inco_obj.write({'afip_code': i})

    @api.one
    def wsfex_update_journals(self, conn_id, test=None):
        pos = self.wsfex_get_web_points_of_sale(conn_id) if not test else {
                test: {
                    'unactive': 'N',
                    'date_to': '',
                }
            }

        jou_mod = self.env['account.journal']

        for po in pos:
            jou = jou_mod.search([
                ('point_of_sale', '=', po),
                ('journal_class_id.afip_code', '=', 19),
                ('journal_class_id.type', '=', 'sale'),
            ])

            if jou:
                continue

            journal_class_e = self.env['afip.journal_class'].search(
                [('afip_code', '=', '019')])
            company = self.env['res.users'].browse(self.env.uid).company_id

            new_sequence = self.env['l10n_ar_invoice.new_sequence']
            new_seq = new_sequence.create({
                    'name': 'Factura [Venta E] (%04i-FVE)' % int(po),
                    'code': 'ws_afip_sequence',
                    'prefix': '%04i' % int(po),
                    'suffix': '-FVE',
                    'company_id': company.id,
                    'builder_id': False })
            new_seq.doit()

            new_journal = self.env['l10n_ar_invoice.new_journal']
            new_jou = new_journal.create({
                    'name': 'Factura [Venta E] (%04i-FVE)' % int(po),
                    'code': 'FVE%04i' % int(po),
                    'type': 'sale',
                    'journal_class_id': journal_class_e.id,
                    'point_of_sale': 1,
                    'sequence_name': 'Factura [Venta E] (%04i-FVE)' % int(po),
                    'company_id': company.id,
                    'currency': False,
                    'builder_id': False })
            new_jou.doit()

    @api.one
    def wsfex_update(self, conn_id):
        self.wsfex_dummy(conn_id)
        self.wsfex_update_countries(conn_id)
        self.wsfex_update_currencies(conn_id)
        self.wsfex_update_invoice_type(conn_id)
        self.wsfex_update_export_type_codes(conn_id)
        self.wsfex_update_units(conn_id)
        self.wsfex_update_languages(conn_id)
        self.wsfex_update_incoterms(conn_id)
        self.wsfex_update_journals(conn_id)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
