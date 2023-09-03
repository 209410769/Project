function Rvr() {
    return (
        <div>
            <section class="search">
                <h2>搜尋房產實價</h2>
                <form>
                    <label for="city">城市：</label>
                    <select id="city" name="city">
                        <option value="台北市">台北市</option>
                        <option value="新北市">新北市</option>
                    </select>
                    <label for="district">區域：</label>
                    <select id="district" name="district">
                        <option value="中正區">中正區</option>
                        <option value="大安區">大安區</option>
                    </select>
                    <label for="address">地址：</label>
                    <input type="text" id="address" name="address" placeholder="請輸入地址" />
                    <input type="submit" value="搜尋" />
                </form>
            </section>

            <section class="results">
                <h2>搜尋結果</h2>
            </section>
        </div>
    );
}

export default Rvr;
