<script setup lang="ts">
import { computed } from 'vue';
import { NProgress, NTooltip, NIcon } from 'naive-ui';
import type { ModernProfile } from '../../../../../types/core';
import { 
  Flash24Filled as EnergyIcon, 
  Emoji24Filled as MoodIcon,
  Warning24Filled as StressIcon,
  Money24Filled as MoneyIcon
} from '@vicons/fluent';

const props = defineProps<{
  profile: ModernProfile;
}>();

const energyColor = computed(() => {
  if (props.profile.energy > 60) return '#18a058';
  if (props.profile.energy > 20) return '#f0a020';
  return '#d03050';
});

const moodColor = computed(() => {
  if (props.profile.mood > 70) return '#18a058';
  if (props.profile.mood < 30) return '#d03050';
  return '#2080f0';
});

const stressColor = computed(() => {
  if (props.profile.stress < 40) return '#18a058';
  if (props.profile.stress < 80) return '#f0a020';
  return '#d03050';
});

</script>

<template>
  <div class="modern-stats">
    <div class="stat-item">
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="icon-wrapper">
             <n-icon :component="EnergyIcon" :color="energyColor" />
             <span class="value">{{ profile.energy }}</span>
          </div>
        </template>
        精力 (Energy)
      </n-tooltip>
      <n-progress 
        type="line" 
        :percentage="profile.energy" 
        :color="energyColor" 
        :show-indicator="false" 
        :height="4"
        class="mini-progress"
      />
    </div>

    <div class="stat-item">
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="icon-wrapper">
             <n-icon :component="MoodIcon" :color="moodColor" />
             <span class="value">{{ profile.mood }}</span>
          </div>
        </template>
        心情 (Mood)
      </n-tooltip>
      <n-progress 
        type="line" 
        :percentage="profile.mood" 
        :color="moodColor" 
        :show-indicator="false" 
        :height="4"
        class="mini-progress"
      />
    </div>

    <div class="stat-item">
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="icon-wrapper">
             <n-icon :component="StressIcon" :color="stressColor" />
             <span class="value">{{ profile.stress }}</span>
          </div>
        </template>
        压力 (Stress)
      </n-tooltip>
      <n-progress 
        type="line" 
        :percentage="profile.stress" 
        :color="stressColor" 
        :show-indicator="false" 
        :height="4"
        class="mini-progress"
      />
    </div>

    <div class="stat-item money">
      <n-tooltip trigger="hover">
        <template #trigger>
          <div class="icon-wrapper">
             <n-icon :component="MoneyIcon" color="#f0a020" />
             <span class="value">¥{{ profile.assets.toLocaleString() }}</span>
          </div>
        </template>
        资产 (Assets)
      </n-tooltip>
    </div>
  </div>
</template>

<style scoped>
.modern-stats {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 0 12px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  height: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 60px;
}

.stat-item.money {
  width: auto;
  min-width: 80px;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  line-height: 1;
  margin-bottom: 2px;
  cursor: help;
}

.value {
  font-family: monospace;
  font-weight: bold;
  color: #eee;
}

.mini-progress {
  width: 100%;
}
</style>
