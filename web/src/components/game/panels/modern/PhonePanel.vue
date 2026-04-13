<script setup lang="ts">
import { ref, computed } from 'vue';
import { NCard, NTabs, NTabPane, NList, NListItem, NAvatar, NButton, NInput, NEmpty } from 'naive-ui';
import type { ModernProfile } from '../../../../../types/core';

const props = defineProps<{
  avatarId: string;
  profile: ModernProfile;
}>();

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
</style>
