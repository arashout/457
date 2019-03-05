#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import matplotlib.pyplot as plt
from os import path
import numpy as np
import seaborn as sns
sns.set()


# In[2]:


df_motion = pd.read_csv(path.join('data','4_increasing.csv'))
df_sensor = pd.read_csv(path.join('data', '4s_increasing.csv'))


# In[3]:


plt.plot(df_sensor.Time, abs(df_sensor.RPM), 'o')


# In[4]:


plt.plot( df_motion.t, df_motion.rpms, 'r.' )


# In[5]:


plt.plot( df_motion.t, df_motion.rpms, 'r.' )
plt.plot(df_sensor.Time, abs(df_sensor.RPM), 'o')


# In[6]:


df_s = df_sensor
df_s.drop(df_s.head(3).index, inplace=True)


# In[9]:


plt.figure(2)
plt.plot(df_motion.t, df_motion.rpms, 'r.', label='Motion')
plt.plot(df_s.Time - 2, abs(df_s.RPM), 'b.', label='Sensor')
plt.title('RPMs vs Time')
plt.ylabel('RPMS')
plt.xlabel('Time [s]')
plt.legend(loc='upper left')
plt.savefig("4_rpm_cmp.png", dpi=600)


# In[ ]:




