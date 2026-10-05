use clothing_mall;

# 주문 테이블의 주문일 컬럼 인덱스 추가
alter table product_order add index idx_order_date(order_date);
# 주문 테이블의 주문일 컬럼 인덱스 삭제
alter table product_order drop index idx_order_date;

# 주문일에 인덱스 추가 여부에 따라 성능 비교
explain analyze
select * from product_order order by order_date desc limit 10;
# 주문일 인덱스 X: type = all / key = null / rows = 16875 / extra = Using filesort
# 주문일 인덱스 O: type = index / key = idx_order_date / rows = 10 / extra = Backward index scan
-- 최종 연산시간 약 4.08ms에서 약 0.06ms로 감소


# 최근 2주일 주문건수 조회 성능 비교
explain analyze
select count(*) as 최근2주간주문건수 from product_order where order_date >= date_sub(now(), interval 2 week); 
# 주문일 인덱스 X: type = all / key = null / rows = 16875 / extra = Using where
# 주문일 인덱스 O: type = range / key = idx_order_date / rows = 223 / extra = Using where; Using index
# 최종 연산시간 약 2.68ms → 약 0.0798ms 


# 최근 1개월 주문건수 조회 성능 비교 
explain analyze
select count(*) as 최근한달주문건수 from product_order where order_date >= date_sub(now(), interval 1 month); 
# 주문일 인덱스 X: type = all / key = null / rows = 16875 / extra = Using where  
# 주문일 인덱스 O: type = range / key = idx_order_date / rows = 974 / extra = Using where; Using index
# 최종 연산시간 약 2.91ms → 약 0.212ms 


# 최근 3개월 주문건수 조회 성능 비교
explain analyze
select count(*) as 최근한달주문건수 from product_order where order_date >= date_sub(now(), interval 3 month); 
# 주문일 인덱스 X: type = all / key = null / rows = 16875 / extra = Using where  
# 주문일 인덱스 O: type = range / key = idx_order_date / rows = 3917 / extra = Using where; Using index
# 최종 연산시간 약 3.66ms → 약 0.798ms 


# 최근 1년 주문건수 조회 성능 비교
explain analyze
select count(*) as 최근한달주문건수 from product_order where order_date >= date_sub(now(), interval 1 year); 
# 주문일 인덱스 X: type = all / key = null / rows = 16875 / extra = Using where  
# 주문일 인덱스 O: type = range / key = idx_order_date / rows = 8437 / extra = Using where; Using index
# 최종 연산시간 약 3.56ms → 약 3.39ms 