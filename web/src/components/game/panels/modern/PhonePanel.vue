<script setup lang="ts">
import { ref, computed } from 'vue';
import { NCard, NTabs, NTabPane, NList, NListItem, NAvatar, NButton, NInput, NEmpty, NTag, NSpace, useMessage } from 'naive-ui';
import type { ModernProfile } from '../../../../../types/core';

const props = defineProps<{
  avatarId: string;
  profile: ModernProfile;
}>();

const message = useMessage();
const loading = ref(false);
const currentEncounter = ref<any>(null);

const handleSwipe = async () => {
  if (props.profile.energy < 15) {
      message.warning("精力不足 (需要 15 点)");
      return;
  }
  loading.value = true;
  try {
    const res = await fetch('/api/social/swipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ avatar_id: props.avatarId })
    });
    const data = await res.json();
    if (data.error) {
        message.error(data.error);
    } else {
        currentEncounter.value = data.encounter;
        if (data.remaining_energy !== undefined) {
            props.profile.energy = data.remaining_energy;
        }
    }
  } catch (e) {
      message.error("网络错误");
  } finally {
      loading.value = false;
  }
};

const handleIceBreak = async (type: string) => {
    if (!currentEncounter.value) return;
    loading.value = true;
    try {
        const res = await fetch('/api/social/ice-break', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                avatar_id: props.avatarId,
                encounter_id: currentEncounter.value.id,
                choice_type: type
            })
        });
        const data = await res.json();
        if (data.success) {
            message.success("加好友成功！已添加到通讯录");
            currentEncounter.value = null;
        } else {
            message.info("对方似乎对你不感兴趣...");
            currentEncounter.value = null;
        }
        if (data.remaining_energy !== undefined) {
            props.profile.energy = data.remaining_energy;
        }
    } catch (e) {
        message.error("网络错误");
    } finally {
        loading.value = false;
    }
};

const activeTab = ref('chat');

// Mock data for now, ideally fetched from API
const chats = ref([
  { id: 1, name: 'Alice', lastMsg: '明天有空吗？', time: '10:30', avatar: '' },
  { id: 2, name: 'Bob', lastMsg: '收到！', time: 'Yesterday', avatar: '' }
]);

const moments = ref([
  { id: 1, name: 'Alice', content: '今天的天气真不错！☀️', time: '1 hour ago', likes: 12, comments: 3 },
  { id: 2, name: 'Charlie', content: '新入职的公司环境很好，加油！', time: '2 hours ago', likes: 5, comments: 0 }
]);

</script>

<template>
  <div class="phone-panel">
    <div class="phone-frame">
      <div class="phone-header">
        <span class="time">12:30</span>
        <div class="status-icons">
          <span>5G</span>
          <span>100%</span>
        </div>
      </div>
      
      <div class="phone-content">
        <n-tabs v-model:value="activeTab" type="segment" animated>
          <n-tab-pane name="chat" tab="微信">
            <n-list clickable hoverable>
              <n-list-item v-for="chat in chats" :key="chat.id">
                <template #prefix>
                  <n-avatar round size="medium" :src="chat.avatar" />
                </template>
                <div class="chat-item">
                  <div class="chat-header">
                    <span class="name">{{ chat.name }}</span>
                    <span class="time-ago">{{ chat.time }}</span>
                  </div>
                  <div class="last-msg">{{ chat.lastMsg }}</div>
                </div>
              </n-list-item>
            </n-list>
          </n-tab-pane>
          
          <n-tab-pane name="moments" tab="朋友圈">
             <div class="moments-feed">
               <div v-for="moment in moments" :key="moment.id" class="moment-card">
                 <div class="moment-header">
                   <n-avatar round size="small" />
                   <span class="name">{{ moment.name }}</span>
                 </div>
                 <div class="moment-content">{{ moment.content }}</div>
                 <div class="moment-footer">
                   <span class="time">{{ moment.time }}</span>
                   <div class="actions">
                     <span>❤️ {{ moment.likes }}</span>
                     <span>💬 {{ moment.comments }}</span>
                   </div>
                 </div>
               </div>
             </div>
          </n-tab-pane>
          
          <n-tab-pane name="contacts" tab="通讯录">
            <n-empty description="暂无联系人" />
          </n-tab-pane>

          <n-tab-pane name="social" tab="探探">
            <div class="social-app">
                <div v-if="!currentEncounter" class="empty-state">
                    <div class="logo">🔥</div>
                    <p>寻找你的心动对象</p>
                    <p class="cost">消耗 15 精力</p>
                    <n-button type="primary" size="large" @click="handleSwipe" :loading="loading">
                        开始匹配
                    </n-button>
                </div>
                <div v-else class="encounter-card">
                    <n-card :title="currentEncounter.name">
                        <n-space vertical>
                            <div class="info-row">
                                <n-tag type="info">{{ currentEncounter.age }}岁</n-tag>
                                <n-tag type="success">{{ currentEncounter.occupation }}</n-tag>
                            </div>
                            <div class="stats-row">
                                <span>颜值: {{ currentEncounter.appearance }}</span>
                                <span>财富: {{ currentEncounter.wealth }}</span>
                            </div>
                            <div class="tags" v-if="currentEncounter.tags">
                                 <n-tag v-for="tag in currentEncounter.tags" :key="tag" size="small" round>
                                     {{ tag }}
                                 </n-tag>
                            </div>
                            <div class="actions">
                                <n-space>
                                    <n-button type="error" ghost @click="currentEncounter = null">Pass</n-button>
                                    <n-button type="primary" @click="handleIceBreak('HUMOR')">幽默</n-button>
                                    <n-button type="primary" @click="handleIceBreak('SINCERE')">真诚</n-button>
                                </n-space>
                            </div>
                        </n-space>
                    </n-card>
                </div>
            </div>
          </n-tab-pane>
        </n-tabs>
      </div>
      
      <div class="phone-home-bar"></div>
    </div>
  </div>
</template>

<style scoped>
.phone-panel {
  position: absolute;
  right: 20px;
  bottom: 20px;
  width: 320px;
  height: 600px;
  pointer-events: auto;
  z-index: 1000;
  filter: drop-shadow(0 0 10px rgba(0,0,0,0.5));
}

.phone-frame {
  width: 100%;
  height: 100%;
  background: #fff;
  border-radius: 30px;
  border: 8px solid #333;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: #f5f5f5;
}

.phone-header {
  height: 30px;
  background: #333;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
  font-size: 12px;
  font-weight: bold;
}

.phone-content {
  flex: 1;
  overflow-y: auto;
  background: #fff;
}

.phone-home-bar {
  height: 20px;
  background: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.phone-home-bar::after {
  content: '';
  width: 100px;
  height: 4px;
  background: #ccc;
  border-radius: 2px;
}

.chat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-header {
  display: flex;
  justify-content: space-between;
}

.name {
  font-weight: bold;
}

.time-ago {
  font-size: 12px;
  color: #999;
}

.last-msg {
  font-size: 12px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.moment-card {
  padding: 12px;
  border-bottom: 1px solid #eee;
  background: #fff;
}

.moment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.moment-content {
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.4;
}

.moment-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.actions {
  display: flex;
  gap: 12px;
}

.social-app {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.logo {
  font-size: 48px;
}

.cost {
  color: #999;
  font-size: 12px;
}

.encounter-card {
  height: 100%;
}

.info-row {
  display: flex;
  gap: 8px;
}

.stats-row {
  display: flex;
  justify-content: space-around;
  font-size: 12px;
  color: #666;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
</style>
