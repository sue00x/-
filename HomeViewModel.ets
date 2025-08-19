import { CommonConstants as Const } from '../common/constants/CommonConstants';
import { isReachNewAchievement, ACHIEVEMENT_LEVEL_KEY , updateTaskOvertimeLevel} from '../model/AchieveModel';
import { TaskMapById, ITaskItem, ACHIEVEMENT_LEVEL_LIST } from '../model/TaskInitList';
import TaskInfo from './TaskInfo';

import DayInfo from './DayInfo';
import { dateToStr, weekDateFormat } from '../common/utils/Utils';
import { WeekDateModel, initializeOnStartUp, getPreviousWeek, getCurMonth, WEEK_DAY_NUM } from '../model/WeekCalendarModel';
import DatabaseApi from '../model/DatabaseModel';
import TaskInfoTableApi from '../common/database/tables/TaskInfoApi';
import DayInfoApi from '../common/database/tables/DayInfoApi';
import GlobalInfoApi from '../common/database/tables/GlobalInfoApi';
import Logger from '../common/utils/Logger';
import GlobalInfo from './GlobalInfo';
import WeekCalendarInfo from './WeekCalendarInfo';
import AchievementInfo from './AchievementInfo';

@Observed
export class HomeStore {
  public currentDate: Date;
  public dateArr: Array<WeekDateModel> = []; // data source list
  public monthArr: WeekDateModel[][] = [];
  public selectedDay: number; // selected day of on week
  public showDate: number;
  public dateTitle: string;
  public selectedDayInfo: WeekDateModel = new WeekDateModel('', '', new Date()); // task info on selected day

  constructor(currentDate: Date) {
    this.currentDate = currentDate;
    this.showDate = currentDate.getTime();
    this.dateTitle = weekDateFormat(currentDate.getTime());
    this.selectedDay = (new Date().getDay() + WEEK_DAY_NUM - 1) % WEEK_DAY_NUM;
  }

  public initData() {
    let weekCalendarInfo: WeekCalendarInfo = initializeOnStartUp(this.currentDate);
    this.dateArr = weekCalendarInfo.arr;
    Logger.info('this.currentDate', this.currentDate.toDateString());
    Logger.info('initWeekData dateArr', JSON.stringify(weekCalendarInfo.strArr))
    // get data form db
    DatabaseApi.query(dateToStr(new Date()), (taskList: TaskInfo[], dayInfo: DayInfo) => {
      Logger.info('Current Day Task Info: ', JSON.stringify(taskList));
      DayInfoApi.queryList(weekCalendarInfo.strArr, (res: DayInfo[]) => {
        let tempList = res.concat(dayInfo);
        Logger.info('initDayInfoList: ', JSON.stringify(res));
        for (let i = 0; i < this.dateArr.length; i++) {
          let tempDayInfo = tempList.find((item: DayInfo) => item.date === this.dateArr[i].dateStr) || new DayInfo(this.dateArr[i].dateStr, 0, 0);
          weekCalendarInfo.arr[i].dayInfo = tempDayInfo;
          if (this.dateArr[i].dateStr === dateToStr(new Date(this.showDate))) {
            // get tasks of showDate
            weekCalendarInfo.arr[i].taskList = taskList;
          }
        }
        this.dateArr = weekCalendarInfo.arr;
        setTimeout(() => {
          this.setSelectedShowDate(this.showDate);
        }, 0)
      })
    })
  }

  public getPreWeekData(date: Date, callback: Function) {
    let weekCalendarInfo: WeekCalendarInfo = getPreviousWeek(date);
    // get data form db
    DayInfoApi.queryList(weekCalendarInfo.strArr, (res: DayInfo[]) => {
      Logger.info('getPreWeekData->DayInfoList: ', JSON.stringify(res));
      if (res.length > 0) {
        for (let i = 0; i < weekCalendarInfo.arr.length; i++) {
          let dayInfo = res.find((item) => item.date === weekCalendarInfo.arr[i].dateStr);
          if (dayInfo) {
            weekCalendarInfo.arr[i].dayInfo = dayInfo;
          }
        }
      }
      this.dateArr = weekCalendarInfo.arr.concat(...this.dateArr);
      callback();
    })
  }

  public loadMonthData(date: Date, callback: Function) {
    // 先用 getCurMonth 拿到按周分组的本月数据
    let monthWeeks: WeekDateModel[][] = getCurMonth(date);

    // 扁平化成一维数组，方便处理
    let allDays: WeekDateModel[] = monthWeeks.flat();

    // 提取所有日期字符串，准备去数据库查询
    let dateStrArr: string[] = allDays.map(item => {
      return item.dateStr;
    });

    // 调用接口查询对应的 DayInfo
    DayInfoApi.queryList(dateStrArr, (res: DayInfo[]) => {
      Logger.info('getCurMonthData->DayInfoList: ', JSON.stringify(res));

      // 把查询结果回填进 allDays
      if (res.length > 0) {
        for (let i = 0; i < allDays.length; i++) {
          let dayInfo = res.find(item => item.date === allDays[i].dateStr);
          if (dayInfo) {
            allDays[i].dayInfo = dayInfo;
          }
        }
      }

      // 回填到 monthWeeks 的二维结构中
      let index = 0;
      for (let w = 0; w < monthWeeks.length; w++) {
        for (let d = 0; d < monthWeeks[w].length; d++) {
          monthWeeks[w][d] = allDays[index++];
        }
      }

      // 更新到 ViewModel（假设你有 monthArr 存储）
      this.monthArr = monthWeeks;

      // 调用回调
      callback();
    });
  }

  // check is current day
  public checkCurrentDay(): boolean {
    return dateToStr(new Date()) === this.selectedDayInfo?.dateStr;
  }

  public updateSelectedDayInfo(selectedDayInfo: WeekDateModel) {
    Logger.debug('updateSelectedDayInfo', JSON.stringify(selectedDayInfo));
    if (selectedDayInfo.taskList?.length === 0) {
      // get data form db
      TaskInfoTableApi.query(selectedDayInfo.dateStr, true, (res: TaskInfo[]) => {
        Logger.info('Selected TaskInfoList: ', JSON.stringify(res));
        selectedDayInfo.taskList = res;
        this.dateArr = this.dateArr.map((item: WeekDateModel) => {
          if(item.dateStr === selectedDayInfo.dateStr) {
            let taskListStr = JSON.stringify(res);
            item.taskList = JSON.parse(taskListStr);
            return item;
          } else {
            return item;
          }
        })
        this.selectedDayInfo = selectedDayInfo;
      });
    } else {
      this.selectedDayInfo = selectedDayInfo;
    }
    Logger.info("selectedDayTaskInfo: ", JSON.stringify(selectedDayInfo.taskList));
  }

  public updateTaskInfoList(editedTaskInfo: ITaskItem) {
    if (editedTaskInfo?.taskID) {
      // edited task
      let taskID = editedTaskInfo.taskID;
      let targetValue = editedTaskInfo.targetValue;
      // 设置初始完成值
      let finValue:string;
      switch (taskID) {
        case 2:
          finValue = '0.00';
          break;
        case 3:
        case 4:
        case 5:
        case 7:
          finValue = '0';
          break;
        default:
          finValue = '';
      }
      let isAlarm = editedTaskInfo.isAlarm;
      let frequency = editedTaskInfo.frequency;
      let startTime = editedTaskInfo.startTime;
      let endTime = editedTaskInfo.endTime;
      let isOpen = editedTaskInfo.isOpen;
      let task = new TaskInfo(0, dateToStr(new Date()), taskID, targetValue, isAlarm,
        startTime, endTime, frequency, false, finValue, isOpen);
      this.dateArr = this.dateArr.map((item: WeekDateModel) => {
        if (task.date === item.dateStr) {
          Logger.info('item', JSON.stringify(item));
          let taskList: TaskInfo[] = item.taskList;
          const dayInfo: DayInfo = item.dayInfo;
          if (editedTaskInfo.isOpen) {
            // add task
            taskList = taskList.filter((taskItem) => taskItem.taskID != taskID)
              .concat(task)
              .sort((a, b) => a.taskID - b.taskID);
            let count: number = 0;
            taskList.forEach((taskItem: TaskInfo) => {
              if (taskItem.isDone) {
                count++;
              }
            });
            if (count > dayInfo.finTaskNum) {
              dayInfo.finTaskNum = count;
            }
          } else {
            // delete task
            let taskIndex = taskList.findIndex((taskItem) => taskItem.taskID === taskID);
            Logger.info('taskList[taskIndex]', JSON.stringify(taskList[taskIndex]));
            if (taskList[taskIndex]?.isDone) {
              dayInfo.finTaskNum -= 1;
            }
            taskList = taskList.filter((taskItem) => taskItem.taskID != taskID);
          }
          dayInfo.targetTaskNum = taskList.length;
          if (dayInfo.finTaskNum > dayInfo.targetTaskNum) {
            dayInfo.finTaskNum = dayInfo.targetTaskNum;
          }
          DayInfoApi.updateData(dayInfo, () => {
          });
          Logger.debug("tempDayInfo", JSON.stringify(dayInfo));
          let weekDateModelStr = JSON.stringify(item);
          let currentDayInfo: WeekDateModel = JSON.parse(weekDateModelStr);
          currentDayInfo.date = item.date;
          currentDayInfo.taskList = taskList;
          currentDayInfo.dayInfo = dayInfo;
          if (this.checkCurrentDay()) {
            this.selectedDayInfo = currentDayInfo;
          }
          return currentDayInfo;
        }
        return item;
      }).slice(0);
    }
  }

  public setSelectedShowDate(showDateTime: number) {
    if (showDateTime > new Date().getTime()) {
      return;
    }
    this.showDate = showDateTime;
    this.dateTitle = weekDateFormat(this.showDate);
    let selectedInfo = this.dateArr.find((item: WeekDateModel) => item.dateStr === dateToStr(new Date(showDateTime)));
    if (selectedInfo) {
      this.updateSelectedDayInfo(selectedInfo);
    }
    Logger.info('dateTitle', this.dateTitle);
  }

  public getDonePercent(): string {
    let dayInfo = this.selectedDayInfo?.dayInfo;
    Logger.debug("dayInfo", JSON.stringify(dayInfo));
    if (dayInfo && (dayInfo?.finTaskNum || 0) > 0) {
      if (dayInfo.finTaskNum > dayInfo.targetTaskNum) {
        return `${Const.DEFAULT_100}`;
      }
      return `${Math.ceil(dayInfo.finTaskNum / dayInfo.targetTaskNum * Const.DEFAULT_100)}`;
    }
    return '0';
  }

  public getTaskListOfDay(): TaskInfo[] {
    Logger.info('getTaskListOfDay', JSON.stringify(this.selectedDayInfo));
    if (this.selectedDayInfo && this.selectedDayInfo.taskList.length > 0) {
      return this.selectedDayInfo.taskList;
    }
    return [];
  }
  // ✅ 新增：检测超量完成的方法
  // private checkOvertimeCompletion(taskItem: TaskInfo): number {
  private checkOvertimeCompletion(taskItem: TaskInfo): number []{

    console.log('--- 超量检测详情 ---');
    console.log(`任务ID: ${taskItem.taskID}`);
    console.log(`完成值: ${taskItem.finValue}`);
    console.log(`目标值: ${taskItem.targetValue}`);

    const fin = Number(taskItem.finValue);
    const target = Number(taskItem.targetValue);

    console.log(`转换后 - 完成值: ${fin}, 目标值: ${target}`);

    // 只检测数值类型的任务
    if (isNaN(fin) || isNaN(target) || target <= 0) {
      console.log('❌ 非数值任务或目标值无效，不检测超量');
      // return 0;
      return [];
    }


    const completionRatio = fin / target;
    console.log(`完成比例: ${completionRatio.toFixed(2)} (${(completionRatio * 100).toFixed(1)}%)`);

    // 根据完成比例返回不同的成就等级
    let achievedLevels: number[] = [];

    if (completionRatio == 2.0) {
      achievedLevels.push(200);
      console.log(' 🥈 达到 200% 成就！');
    }

    if (completionRatio == 4.0) {
      achievedLevels.push(400);
      console.log('🥇 达到 400% 成就！');
    }

    if (completionRatio >= 10.0) {
      achievedLevels.push(1000);
      console.log('🏆 达到 1000% 非凡大师 成就！');
    }

    console.log('达到的所有等级:', achievedLevels);
    return achievedLevels;
  }

  public async taskClock(taskInfo: TaskInfo) {
    let taskItem = await this.updateTask(taskInfo);
    let dateStr = this.selectedDayInfo?.dateStr;
    if (!taskItem) {
      return {
        achievementLevel: 0,
        showAchievement: false
      } as AchievementInfo;
    }
    // 检测超量完成
    // let overtimeAchievement: number = 0;
    let overtimeAchievements: number[] = [];  // 改为数组
    let maxOvertimeLevel = 0;
    if (taskItem.isDone) {
      console.log('=== 检测超量完成 ===');
      overtimeAchievements = this.checkOvertimeCompletion(taskItem);
      if (overtimeAchievements.length > 0) {
        
        for (let level of overtimeAchievements) {
          updateTaskOvertimeLevel(taskItem.taskID, level);
        }
        // 获取最高等级用于弹窗显示
        maxOvertimeLevel = Math.max(...overtimeAchievements);
        console.log(`任务${taskItem.taskID}超量完成！达到等级: ${overtimeAchievements.join(', ')}`);
        Logger.info(`任务${taskItem.taskID}超量完成！达到等级: ${overtimeAchievements.join(', ')}`);
      } else {
        console.log(`任务${taskItem.taskID}正常完成，无超量成就`);
      }
    }
    this.selectedDayInfo.taskList = this.selectedDayInfo.taskList.map((item) => {
      return item.taskID === taskItem?.taskID ? taskItem : item;
    });
    // 检查连续打卡成就
    let achievementLevel: number = 0;
    if (taskItem.isDone) {
      let dayInfo = await this.updateDayInfo();
      if (dayInfo && dayInfo?.finTaskNum === dayInfo?.targetTaskNum) {
        achievementLevel = await this.updateAchievement(this.selectedDayInfo.dayInfo);
        // 特殊处理：连续1天打卡成功
        if (achievementLevel === 1) {
          console.log('首次打卡成功！显示特殊弹窗');
        }
      }
    }


    this.dateArr = this.dateArr.map((item: WeekDateModel) => dateStr === item.dateStr ? this.selectedDayInfo : item);
    // ✅ 修改：优先显示超量成就，否则显示连续打卡成就
    const finalAchievementLevel = maxOvertimeLevel > 0 ? maxOvertimeLevel : achievementLevel;
    const shouldShowAchievement = maxOvertimeLevel > 0 || ACHIEVEMENT_LEVEL_LIST.includes(achievementLevel);


    return {
      achievementLevel: finalAchievementLevel,
      showAchievement: shouldShowAchievement,
      isFirstDay: achievementLevel === 1
    } as AchievementInfo;
  }

  updateTask(task: TaskInfo): Promise<TaskInfo> {
    return new Promise((resolve, reject) => {
      let taskID = task.taskID;
      let targetValue = task.targetValue;
      let finValue = task.finValue;
      let updateTask = new TaskInfo(task.id, task.date, taskID, targetValue, task.isAlarm, task.startTime,
        task.endTime, task.frequency, task.isDone, finValue, task.isOpen);
      let step = TaskMapById[taskID - 1].step;

      if (step === 0) {
        // 一次性任务：点击一次就完成
        updateTask.isDone = true;
        updateTask.finValue = targetValue;
      } else {
        // 数值累加任务：支持超量完成
        let value = Number(finValue) + step;
        updateTask.isDone = value >= Number(targetValue); // ✅ 重新计算是否完成
        updateTask.finValue = `${value}`; // ✅ 允许超过目标值
      }

      TaskInfoTableApi.updateDataByDate(updateTask, (res: number) => {
        // ✅ 修改：只检查数据库更新是否成功，不检查是否已完成
        if (!res) {
          Logger.error('taskClock-updateTask', JSON.stringify(res));
          reject(res);
        } else {
          resolve(updateTask);
        }
      })
    })
  }

  updateDayInfo(): Promise<DayInfo> {
    let dayInfo: DayInfo = this.selectedDayInfo.dayInfo;
    dayInfo.finTaskNum += 1;
    dayInfo.targetTaskNum = this.selectedDayInfo.taskList.length;
    return new Promise((resolve, reject) => {
      DayInfoApi.updateData(dayInfo, (res: number) => {
        if (!res) {
          Logger.error('taskClock-updateDayInfo', JSON.stringify(res));
          reject(res);
        }
        Logger.info('taskClock-updateDayInfo', JSON.stringify(dayInfo));
        // 同步界面数据
        let dayInfoStr = JSON.stringify(dayInfo);
        this.selectedDayInfo.dayInfo = JSON.parse(dayInfoStr);
        resolve(dayInfo);
      });
    });
  }

  updateAchievement(dayInfo: DayInfo): Promise<number> {
    Logger.debug('taskClock-updateAchievement', JSON.stringify(dayInfo));
    return new Promise((resolve, reject) => {
      let preDay = new Date();
      preDay.setDate(preDay.getDate() - 1);
      preDay = new Date(preDay);
      let preDayStr = dateToStr(preDay);
      Logger.info('taskClock-updateAchievement-1', `${preDayStr}`);
      DayInfoApi.query(preDayStr, (res: DayInfo) => {
        Logger.info('taskClock-updateAchievement-2', JSON.stringify(res));
        let isReset = res?.date === '' || res?.targetTaskNum > res?.finTaskNum;
        GlobalInfoApi.query((res: GlobalInfo) => {
          Logger.info('taskClock-globalInfoApi', JSON.stringify(res));
          let achievementInfo = res;
            isReset ? (achievementInfo.checkInDays = 1) : (achievementInfo.checkInDays += 1);
          let isNewAchieve = isReachNewAchievement(achievementInfo);
          let isFirstDaySuccess = achievementInfo.checkInDays === 1 && isNewAchieve;

          if (isNewAchieve) {
            AppStorage.SetOrCreate(ACHIEVEMENT_LEVEL_KEY, achievementInfo.checkInDays);
            achievementInfo.achievements = achievementInfo.achievements + ',' + achievementInfo.checkInDays;
            if (isFirstDaySuccess) {
              console.log('🎉 恭喜！首次连续1天打卡成功！');
              // 这里可以触发特殊的弹窗或动画
            }
          }
          // 保存到数据库
          GlobalInfoApi.updateData(achievementInfo, (res: number) => {
            if (!res) {
              Logger.error('taskClock-updateAchievement', JSON.stringify(res));
              reject(res);
            }
            Logger.debug('taskClock-updateAchievement', JSON.stringify(achievementInfo));
              // isNewAchieve ? resolve(achievementInfo.checkInDays) : resolve(0);
            if (isNewAchieve) {
              console.log(`🏆 新成就解锁：连续${achievementInfo.checkInDays}天打卡！`);
              resolve(achievementInfo.checkInDays);
            } else {
              resolve(0);
            }
          });
        });
      })
    });
  }
}

