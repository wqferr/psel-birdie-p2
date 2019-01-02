
# coding: utf-8

# In[1]:


import pandas as pd
from smartphone_features import series_to_attr


# In[2]:


data = pd.read_csv('smartphones.tsv', sep='\t')
data.set_index('ID', inplace=True)
data.head()


# In[3]:


attr = series_to_attr(data.TITLE)
attr.head()


# In[5]:


print('Celulares com marcas conhecidas, mas modelos não identificados:')
attr[(attr.MODEL.isnull()) & (~attr.BRAND.isnull())]


# In[6]:


print('Celulares com marcas não reconhecidas:')
attr[attr.BRAND.isnull()]


# In[7]:


print(f'Total de modelos não identificados: {attr.MODEL.isnull().sum()} de {data.shape[0]}')


# In[8]:


attr.to_csv('features.tsv', sep='\t', na_rep='N/A')

