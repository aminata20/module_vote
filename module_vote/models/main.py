# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from operator import itemgetter 

from collections import Counter # Get Counter


class CreateVote(models.Model):
    _name = 'etudiant.etudiant'
    _rec_name = 'votant'
    

    ### Event fields
    event_name = fields.Many2one(string=u'Choisissez un évènement', comodel_name='ev.ev')

    ### Votant fields
    votant = fields.Char(default=lambda self:self.env.user.name)

    ### Vote fields
    etd_1 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°1", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    
    etd_2 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°2", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_3 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°3", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_4 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°4", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_5 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°5", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_6 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°6", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_7 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°7", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_8 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°8", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_9 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°9", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])    
    etd_10 = fields.Many2one(comodel_name='res.users', string="Voter l'étudiant N°10", required=True, domain=lambda self:[('id','!=',2),('id','!=',self.env.uid)])

    
    ### Constrains => oneVote for oneEvent / student
    _sql_constraints = [('votant_event_name_unique', 'UNIQUE(votant,event_name)', 'Désolé,\nVous avez déjà validé un vote pour cet évènement.')]


    #### les contraintes empêchant de voter 2 fois la même personne ###
    @api.one
    @api.constrains('etd_1','etd_2','etd_3','etd_4','etd_5','etd_6','etd_7','etd_8','etd_9','etd_10')
    def _block_1(self):
        for rec in self:
            self.checkin = []
            self.etd_voted = [rec.etd_1, rec.etd_2, rec.etd_3, rec.etd_4, rec.etd_5, rec.etd_6, rec.etd_7, rec.etd_8, rec.etd_9, rec.etd_10]
            for vv in self.etd_voted:
                self.checkin.append(vv.id)
            for i in self.checkin:
                if self.checkin.count(i) >= 2:
                    raise ValidationError("Désolé, vous avez voté plusieurs fois un même étudiant.\nChoisissez un autre candidat.")
                break


class VoirGagnant(models.Model):
    _name = 'win.win'
    _description = 'Gagnant'
    _rec_name = 'evenements'
        

    evenements = fields.Many2one(comodel_name='ev.ev', string="Choisissez un évènement")
    winner_1 = fields.Char(string='Vainqueur', compute='_winner_1', store=True)

    c_k_1 = fields.Char(string="# 1", compute="_get_kv", store=True, readonly=True)
    c_k_2 = fields.Char(string="# 2", compute="_get_kv", store=True, readonly=True)
    c_k_3 = fields.Char(string="# 3", compute="_get_kv", store=True, readonly=True)
    c_k_4 = fields.Char(string="# 4", compute="_get_kv", store=True, readonly=True)
    c_k_5 = fields.Char(string="# 5", compute="_get_kv", store=True, readonly=True)


    #
    @api.depends('evenements')
    def _winner_1(self):
        #
        w_ = 0
        scrutin = dict()
        tab_n = list()
        #
        ev_vote = list()
        ev_tab = list()
        #
        maxi = 0
        win = list()
    
        for rec in self:
            rec.vainqueur = self.evenements.id
            ev_vote = self.env['etudiant.etudiant'].sudo().search([['event_name','=',rec.evenements.id]])
            for i in ev_vote:
                ev_tab.append(i.etd_1.id)
                ev_tab.append(i.etd_2.id)
                ev_tab.append(i.etd_3.id)
                ev_tab.append(i.etd_4.id)
                ev_tab.append(i.etd_5.id)
                ev_tab.append(i.etd_6.id)
                ev_tab.append(i.etd_7.id)
                ev_tab.append(i.etd_8.id)
                ev_tab.append(i.etd_9.id)
                ev_tab.append(i.etd_10.id)

            for i in ev_tab:
                w_st = self.env['res.users'].search([['id','=',i]])
                _name = w_st.name
                tab_n.append(_name)
            # Make a scrutin => {nom: nombre_de_vote}
            for nm in set(tab_n):
                nb_voted = tab_n.count(nm)
                member = {nm:nb_voted}
                scrutin.update(member)
            # Get the Winner.s
            for item in scrutin.items():
                if item[-1] > maxi:
                    maxi = item[-1]
            for i in scrutin.items():
                if maxi == i[-1]:
                    win.append(i[0])
                w_ = win
            rec.winner_1 = w_

    #
    @api.depends('evenements')
    def _get_kv(self):
        #
        scrutin = dict()
        tab_n = list()
        #
        ev_vote = list()
        ev_tab = list()
        #
        
        for rec in self:
            rec.vainqueur = self.evenements.id
            ev_vote = self.env['etudiant.etudiant'].sudo().search([['event_name','=',rec.evenements.id]])
            for i in ev_vote:
                ev_tab.append(i.etd_1.id)
                ev_tab.append(i.etd_2.id)
                ev_tab.append(i.etd_3.id)
                ev_tab.append(i.etd_4.id)
                ev_tab.append(i.etd_5.id)
                ev_tab.append(i.etd_6.id)
                ev_tab.append(i.etd_7.id)
                ev_tab.append(i.etd_8.id)
                ev_tab.append(i.etd_9.id)
                ev_tab.append(i.etd_10.id)

            for i in ev_tab:
                w_st = self.env['res.users'].search([['id','=',i]])
                _name = w_st.name
                tab_n.append(_name)
            # Make a scrutin => {nom: nombre_de_vote}
            for nm in set(tab_n):
                nb_voted = tab_n.count(nm)
                member = {nm:nb_voted}
                scrutin.update(member)
            # Get the 5 best in the scrutin
            k = Counter(scrutin)
            five = k.most_common(5)
            #
            rec.c_k_1 = str(five[0][0]) + " - " + str(five[0][1])
            #
            rec.c_k_2 = str(five[1][0]) + " - " + str(five[1][1])
            #
            rec.c_k_3 = str(five[2][0]) + " - " + str(five[2][1])
            #
            rec.c_k_4 = str(five[3][0]) + " - " + str(five[3][1])
            #
            rec.c_k_5 = str(five[4][0]) + " - " + str(five[4][1])

# Module Evenement
class EventEvent(models.Model):
    _name = 'ev.ev'
    _description = 'Evenement'
    _order = 'date_begin'


    #names
    name = fields.Char(string='Evenement', required=True, readonly=False )

    # Date fields
    date_begin = fields.Datetime(string='Date de debut', required=True)
    date_end = fields.Datetime(string='Date de fin', required=True)


    @api.one
    @api.constrains('date_begin', 'date_end')
    def _check_closing_date(self):
        if self.date_end < self.date_begin:
            raise ValidationError(_('la date de debut doit être avant celle de fin.'))

    @api.multi
    @api.depends('name', 'date_begin', 'date_end')
    def name_get(self):
        result = []
        for event in self:
            date_begin = fields.Datetime.from_string(event.date_begin)
            date_end = fields.Datetime.from_string(event.date_end)
            dates = [fields.Date.to_string(fields.Datetime.context_timestamp(event, dt)) for dt in [date_begin, date_end] if dt]
            dates = sorted(set(dates))
            result.append((event.id, '%s (%s)' % (event.name, ' - '.join(dates))))
        return result