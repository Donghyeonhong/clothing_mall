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

-- 따라서 일정 기간 주문건수 조회를 위해 주문일에 인덱스를 추가하는 것이 필요하다고 판단된다.


# (member_id, order_date) 복합인덱스 생성
create index idx_member_order_date
on product_order(member_id, order_date);
# (member_id, order_date) 복합인덱스 삭제
alter table product_order drop index idx_member_order_date;


# 특정 회원(회원번호 253번)의 주문 내역을 최신순으로 조회 성능
explain analyze
SELECT *
FROM product_order
WHERE member_id = 253
ORDER BY order_date DESC;

-- 실행시간: 약 0.0402, 0.0319, 0.0356, 0.0309
-- 한 사람당 주문이 2~3개 정도 
-- 외래키 member_id는 기본적으로 인덱스를 보유
-- 개별 인덱스를 사용하면 member_id 인덱스를 통해 특정 회원의 주문을 찾은 후 
-- 해당 주문들의 order_date를 별도로 정렬하여 조회

-- (member_id, order_date) 복합인덱스를 사용하면 member_id로 해당 회원의 주문 범위를 찾고 
-- order_date가 인덱스에 정렬된 상태이므로 별도 정렬 과정없이 역방향으로 스캔하여 최신 주문부터 조회
 
-- 하지만 특정 회원의 주문건수는 인당 2~3건이어서 개별인덱스와 복합인덱스의 성능차이는 차이가 거의 없었으며,
-- (member_id, order_date)복합인덱스 설정은 필요하지 않은 것으로 판단된다.


# join분석
# 회원번호 253번의 주문내역 조회 성능 분석
explain analyze
SELECT
    o.order_id,
    p.product_name,
    po.size,
    d.Quantity,
    d.unit_price,
    o.order_date
FROM product_order o
JOIN order_detail d
    ON o.order_id = d.order_id
JOIN product_option po
    ON d.option_id = po.option_id
join product p
	on po.product_id = p.product_id
WHERE o.member_id = 253;

-- 1. 인덱스 idx_member_id로 253번 회원의 주문 3개 찾기
-- 2. 조인과 PK(order_id, option_id)의 첫 번째 컬럼인 order_id를 통해 주문 3개에 대한 상세주문 6개 찾기
-- 3. 상세주문 6개 option_id에 대해 1대1로 product_option 정보 조회
-- 4. product_option에서 얻은 product_id를 가지고 1대1로 product 정보 조회

-- 실행시간은 약 0.0889ms로 측정됐으며, 
-- join 조건에 사용되는 컬럼에 적절한 인덱스가 적용된 상태여서 추가적인 인덱스 설정은 필요하지 않은 것으로 판단
