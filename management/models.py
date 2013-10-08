from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from datetime import timedelta
from datetime import date


class Client(models.Model):
    name = models.CharField('company name', max_length=50)
    contact_name = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    #created_by = models.ForeignKey(User)
    #modified_by = models.ForeignKey(User)
    #models.ForeignKey(User, default=request.user)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'pk': self.id})


class Title(models.Model):
    client = models.ForeignKey(Client)
    name = models.CharField('title', max_length=50)
    job_number = models.CharField(max_length=25, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('title-detail', kwargs={'pk': self.id})



class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class ProductStatus(models.Model):
    status = models.CharField('status name', max_length=50)
    color = models.CharField('hex color', max_length=20, blank=True)
    finalised = models.BooleanField('mark product as complete', default=False)
    display_order = models.IntegerField(default=1)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name_plural = 'product status'

class Product(models.Model):
    title = models.ForeignKey(Title)
    product_type = models.ForeignKey(ProductType)
    name = models.CharField('description', max_length=50, blank=True, help_text='eg. Special Edition')  
    cat_number = models.CharField('catalogue number', max_length=20, blank=True)
    due_date = models.DateField()
    status = models.ForeignKey(ProductStatus)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def _get_full_name(self):
        if self.name == '':
            return u'%s %s' % (self.title.name, self.product_type.name)
        else:
            return u'%s %s %s' % (self.title.name, self.product_type.name, self.name)

    full_name = property(_get_full_name)

    def date_status(self):

        num_days = self.due_date - date.today()
        num_days = int(num_days.days)
        
        if num_days <= 0:
            return "reporttext-attention"
        elif num_days < 3:
            return "reporttext-progress"
        else:
            return ''


    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'product_id': self.id})

    def __unicode__(self):
        return self.full_name


