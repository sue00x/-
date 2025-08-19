/*
 * Copyright (c) 2023 Huawei Device Co., Ltd.
 * Licensed under the Apache License,Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import CardInfo from './CardInfo';
import { ACHIEVEMENT_LEVEL_LIST, AchievementMap, ACHIEVEMENT_LEVEL_LIST_single } from '../model/TaskInitList';
import { TASK_OVERTIME_LEVELS,hasTaskAchievedOvertimeLevel,getTaskOvertimeKey } from '../model/AchieveModel'
import Logger from '../common/utils/Logger'

// export function getBadgeCardItems_single(successiveDays: number): Array<CardInfo> {
//   let badgeMileStones_single = ACHIEVEMENT_LEVEL_LIST_single;
//   const overtimeLevels: number[] = TASK_OVERTIME_LEVELS;
//
//   let cardItems: Array<CardInfo> = [];
//   for (let i = 0; i < badgeMileStones_single.length; i++) {
//     let onOrOff = successiveDays >= badgeMileStones_single[i] ? 'on' : 'off';
//     let titleContent = String(badgeMileStones_single[i]);
//     let cardInfo: CardInfo = new CardInfo();
//     cardInfo.titleContent = titleContent;
//     cardInfo.achievement = getAchievement(`${onOrOff}_${badgeMileStones_single[i]}`);
//     cardItems.push(cardInfo);
//   }
//   return cardItems;
// }


// export function getBadgeCardItems_single(successiveDays: number): Array<CardInfo> {
//   let badgeMileStones_single = ACHIEVEMENT_LEVEL_LIST_single;
//   let cardItems: Array<CardInfo> = [];
//
//   for (let i = 0; i < badgeMileStones_single.length; i++) {
//     let level = badgeMileStones_single[i];
//
//     // 🔥 关键修改：检查是否有任何任务达到了这个超额等级
//     let onOrOff = 'off';
//
//     // 首先检查连续天数成就
//     if (successiveDays >= level) {
//       onOrOff = 'on';
//     } else {
//       // 检查是否有任何任务达到了超额完成
//       let hasAnyTaskOvertime = checkAnyTaskHasOvertime(level);
//       console.log('hasAnyTaskOvertime:', hasAnyTaskOvertime);
//
//       if (hasAnyTaskOvertime) {
//         onOrOff = 'on';
//       }
//     }
//
//     let titleContent = String(level);
//     let cardInfo: CardInfo = new CardInfo();
//     cardInfo.titleContent = titleContent;
//     cardInfo.achievement = getAchievement(`${onOrOff}_${level}`);
//     cardItems.push(cardInfo);
//   }
//   return cardItems;
// }

export function getBadgeCardItems_single(successiveDays: number, taskID: number): Array<CardInfo> {
  let badgeMileStones_single = ACHIEVEMENT_LEVEL_LIST_single;
  let cardItems: Array<CardInfo> = [];

  for (let i = 0; i < badgeMileStones_single.length; i++) {
    let level = badgeMileStones_single[i];

    // 🔥 关键修改：只检查特定任务的超额完成状态
    let onOrOff = 'off';

    // 首先检查连续天数成就
    if (successiveDays >= level) {
      onOrOff = 'on';
    } else {
      // 只检查当前任务是否达到了超额完成
      let hasThisTaskOvertime = hasTaskAchievedOvertimeLevel(taskID, level);
      console.log(`任务${taskID}是否达到${level}%超额:`, hasThisTaskOvertime);

      if (hasThisTaskOvertime) {
        onOrOff = 'on';
      }
    }

    let titleContent = String(level);
    let cardInfo: CardInfo = new CardInfo();
    cardInfo.titleContent = titleContent;
    cardInfo.achievement = getAchievement(`${onOrOff}_${level}`);
    cardItems.push(cardInfo);
  }

  return cardItems;
}

function checkAnyTaskHasOvertime(milestone: number): boolean {
  // 检查所有相关任务是否有超额完成
  const taskIDs = [2, 3, 4, 7]; // 喝水、吃苹果、微笑任务ID（根据你的TaskMapById）

  for (let taskID of taskIDs) {
    if (hasTaskAchievedOvertimeLevel(taskID, milestone)) {
      return true; // 有任务达到这个超额等级
    }
  }
  return false;
}

export function getAchievement(key: string) {
  let result = $r('app.string.empty');
  switch (key) {
    // case 'off_100':
    //   result = AchievementMap.off_100;
    //   break;
    // case 'on_100':
    //   result = AchievementMap.on_100;
    //   break;
    case 'off_200':
      result = AchievementMap.off_200;
      break;
    case 'on_200':
      result = AchievementMap.on_200;
      break;
    case 'off_300':
      result = AchievementMap.off_300;
      break;
    case 'on_300':
      result = AchievementMap.on_300;
      break;
    case 'off_400':
      result = AchievementMap.off_400;
      break;
    case 'on_400':
      result = AchievementMap.on_400;
      break;
    // case 'off_1000':
    //   result = AchievementMap.off_1000;
    //   break;
    case 'on_1000':
      result = AchievementMap.on_1000;
      break;

    default:
      break;
  }
  return result;
}